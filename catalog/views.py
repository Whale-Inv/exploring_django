from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.views import View
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Category


class ProductListView(ListView):
    model = Product

    def get_paginate_by(self, queryset):
        """Определяем количество товаров на странице"""
        # Получаем значение из GET или используем 6 по умолчанию
        per_page = self.request.GET.get('per_page', '6')

        try:
            per_page = int(per_page)
            # Проверяем разрешенные значения
            if per_page in [3, 6, 12]:
                return per_page
        except (ValueError, TypeError):
            pass

        # Если что-то пошло не так, возвращаем 12
        return 6

    def get_queryset(self):
        """Сортировка и фильтрация"""
        queryset = super().get_queryset()
        # Добавьте фильтрацию, если нужно
        # queryset = queryset.filter(is_active=True)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Расширяем контекст"""
        context = super().get_context_data(**kwargs)

        # Динамическая пагинация
        per_page = self.request.GET.get('per_page', 6)
        try:
            per_page = int(per_page)
            if per_page not in [3, 6, 12]:
                per_page = 3
        except (ValueError, TypeError):
            per_page = 6

        # Обновляем paginate_by
        self.paginate_by = per_page

        # Получаем queryset заново с новым paginate_by
        queryset = self.get_queryset()
        paginator = Paginator(queryset, per_page)
        page = self.request.GET.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['products'] = products
        context['per_page'] = per_page
        context['page_obj'] = products  # для совместимости с шаблонами
        context['paginator'] = paginator

        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    login_url = reverse_lazy('users:login')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')


def home(request):
    # Получаем последние 5 продуктов
    latest_products = Product.objects.all().order_by('-id')[:5]

    # Выводим в консоль
    print(f"\nПоследние 5 продуктов (всего в базе: {Product.objects.count()}):")
    for product in latest_products:
        print(f"  - {product.product_name}")
    return render(request, "catalog/home.html", {'products': latest_products})


class ContactView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")

        # Контекст для шаблона
        context = {
            'name': name,
            'phone': phone,
            'message': message,
        }

        # Рендерим шаблон успешной отправки
        return render(request, "catalog/contact_success.html", context)

