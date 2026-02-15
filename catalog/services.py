from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """ Получает данные о продуктах из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Product.objects.filter(is_published=True).order_by('-created_at')

    key = "products_list"
    products = cache.get(key)

    if products is not None:
        return products

    # Сохраняем в кэш уже отфильтрованный и отсортированный queryset
    products = Product.objects.filter(is_published=True).order_by('-created_at')
    cache.set(key, products)
    return products


def get_products_by_category(category_id):
    """Возвращает все продукты указанной категории"""
    return Product.objects.filter(category_id=category_id, is_published=True)