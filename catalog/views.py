from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from catalog.models import Product, Category


# def product_list(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'products_list.html', context)


def product_list(request):
    """Список товаров с пагинацией"""

    # Получаем все товары (можно добавить фильтрацию)
    products_list = Product.objects.all().order_by('-created_at')

    # Получаем номер страницы из GET-параметра
    page = request.GET.get('page', 1)

    # Количество товаров на странице
    per_page = request.GET.get('per_page', 6)  # можно менять через GET

    try:
        per_page = int(per_page)
        if per_page not in [3, 6, 12]:
            per_page = 3
    except ValueError:
        per_page = 12

    # Создаем пагинатор
    paginator = Paginator(products_list, per_page)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если page не целое число, показываем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если page выходит за диапазон, показываем последнюю страницу
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'per_page': per_page,
    }

    return render(request, 'products_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_detail.html', context)


def home(request):
    # Получаем последние 5 продуктов
    latest_products = Product.objects.all().order_by('-id')[:5]

    # Выводим в консоль
    print(f"\nПоследние 5 продуктов (всего в базе: {Product.objects.count()}):")
    for product in latest_products:
        print(f"  - {product.product_name}")
    return render(request, "home.html", {'products': latest_products})


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(name)
        print(phone)
        print(message)
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено")
    return render(request, "contacts.html")


def add_product(request):
    """Ручная обработка формы"""
    categories = Category.objects.all()

    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        # Валидация
        errors = []
        if not name:
            errors.append('Введите название товара')
        if not price or int(price) <= 0:
            errors.append('Цена должна быть положительной')

        if not errors:
            # Создаем товар
            try:
                category = None
                if category_id:
                    category = Category.objects.get(id=category_id)
                product = Product.objects.create(
                    product_name=name,
                    description=description,
                    price=price,
                    category=category,
                    image=image,
                )
                messages.success(request, f'Товар "{name}" добавлен!')
                return redirect('product_detail', pk=product.pk)
            except Exception as e:
                errors.append(f'Ошибка: {e}')

        # Если есть ошибки
        context = {
            'errors': errors,
            'name': name,
            'description': description,
            'price': price,
            'category_id': category_id,
            'categories': categories,
        }
        return render(request, 'catalog/add_product.html', context)

    return render(request, 'add_product.html', {
        'categories': categories  # ВАЖНО: передаем категории
    })
