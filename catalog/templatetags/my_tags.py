from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.filter
def bullet_list(value):
    """Преобразует строки с - в маркированный список"""
    lines = value.split('\n')
    result = []

    for line in lines:
        line = line.strip()
        if line.startswith('-'):
            result.append(f'<li>{line[1:].strip()}</li>')
        elif line:
            result.append(f'<p>{line}</p>')

    if any('<li>' in line for line in result):
        # Нашли элементы списка
        html = []
        i = 0
        while i < len(result):
            if '<li>' in result[i]:
                # Начало списка
                html.append('<ul>')
                while i < len(result) and '<li>' in result[i]:
                    html.append(result[i])
                    i += 1
                html.append('</ul>')
            else:
                html.append(result[i])
                i += 1
        return mark_safe(''.join(html))

    return mark_safe(''.join(result))


@register.filter
def price_with_currency(value, currency="₽"):
    """Форматирует цену с валютой"""
    try:
        if isinstance(value, str):
            value = float(value.replace(',', '.'))

        # Разделяем тысячи пробелами
        formatted = f"{value:,.0f}".replace(',', ' ')
        return f"{formatted} {currency}"

    except:
        return f"{value} {currency}"


@register.filter
def price_detailed(value):
    """Подробное форматирование с копейками"""
    try:
        if isinstance(value, str):
            value = float(value.replace(',', '.'))

        # Целая часть
        int_part = int(value)
        # Дробная часть (копейки)
        fractional = int(round((value - int_part) * 100))

        # Форматируем целую часть с пробелами
        int_formatted = f"{int_part:,}".replace(',', ' ')

        if fractional > 0:
            return f"{int_formatted},{fractional:02d} ₽"
        else:
            return f"{int_formatted} ₽"

    except:
        return f"{value} ₽"