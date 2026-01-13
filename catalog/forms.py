from django import forms

from catalog.models import Category


class ProductForm(forms.Form):
    product_name = forms.CharField(
        max_length=200,
        label='Название товара',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название товара'
        })
    )
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Подробное описание товара...'
        })
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Цена (₽)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '1',
            'min': '100'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        required=False,
        label='Изображение',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    create_at = forms.DateTimeField(
        auto_now_add=True
    )
    update_at = forms.DateTimeField(
        auto_add=True
    )