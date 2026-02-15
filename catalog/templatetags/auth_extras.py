from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """Проверяет, принадлежит ли пользователь к указанной группе"""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()