from django.core.management.base import BaseCommand
from django.core.management import call_command
from unicodedata import category

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        category1, _ = Category.objects.get_or_create(category_name='Бакалея')

        products = [
            {'product_name': 'Улитка греческая', 'description': 'с курицей и картошкой', 'price': 75, 'category': category1},
            {'product_name': 'Батон', 'description': 'нарезной, белый',  'price': 54, 'category': category1},
            {'product_name': 'Хлеб', 'description': 'бородинский',  'price': 55, 'category': category1},
        ]

        for product in products:
            product, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.product_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.product_name}'))

        category2, _ = Category.objects.get_or_create(category_name='Молочная продукция')

        products = [
            {'product_name': 'Кефир', 'description': '1%, полезен для пищеварения',  'price': 89, 'category': category2},
            {'product_name': 'Молоко', 'description': 'жирность 3,2%',  'price': 92, 'category': category2},
            {'product_name': 'Йогурт', 'description': 'черничный',  'price': 56, 'category': category2},
        ]

        for product in products:
            product, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.product_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Product already exists: {product.product_name}'))