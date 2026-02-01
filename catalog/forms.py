import os

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from catalog.models import Product, Category


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].help_text = None
        self.fields['category'].label = 'Категория'
        self.fields['price'].label = 'Цена'

        self.fields['product_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите название товара'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание товара'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите цену'})

    def clean(self):
        ban_words = ['казино','криптовалюта','крипта','биржа','дешево','бесплатно','обман','полиция','радар']
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        description = cleaned_data.get('description')

        for word in ban_words:
            if word in product_name.lower():
                self.add_error('product_name', f'Недопустимое слово: {word}')
            if word in description.lower():
                self.add_error('description', f'Недопустимое слово: {word}')
        return cleaned_data

    def clean_price(self):
        """ Валидация поля price """
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError("Цена введена неправильно")
        return price

    def clean_image(self):
        """Валидация поля image"""
        image = self.cleaned_data.get('image')

        # Допустимые расширения
        valid_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']

        # Получаем расширение файла
        ext = os.path.splitext(image.name)[1]

        if ext not in valid_extensions:
            raise ValidationError("Поддерживаются только файлы в формате JPEG или PNG")

        # Проверка размера не более 5 МБ
        max_size = 5 * 1024 * 1024
        if image.size > max_size:
            raise ValidationError(
                f'Размер файла не должен превышать 5 МБ. Текущий размер: {image.size / (1024 * 1024):.2f} МБ'
            )
        return image