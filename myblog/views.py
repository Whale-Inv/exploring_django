from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from myblog.models import MyPosts


class PostListView(ListView):
    model = MyPosts
    template_name = 'myblog/post_list.html'

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

        # Если что-то пошло не так, возвращаем 6
        return 6

    def get_queryset(self):
        """Сортировка и фильтрация"""
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
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


class PostDetailView(DetailView):
    model = MyPosts
    template_name = 'myblog/post_detail.html/'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1

        if self.object.views_count == 100:
            from django.core.mail import send_mail
            from django.conf import settings

            send_mail(
                subject=f'🎉 100 просмотров! "{self.object.title}"',
                message=f'Поздравляем! Ваш пост достиг 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
            )
            print("Письмо отправлено!")

        self.object.save()
        return self.object



class PostCreateView(CreateView):
    model = MyPosts
    template_name = 'myblog/post_form.html'
    fields = ["title", "content", "image", "is_published"]
    success_url = reverse_lazy('myblog:post_list')


class PostUpdateView(UpdateView):
    model = MyPosts
    template_name = 'myblog/post_form.html'
    fields = ["title", "content", "image", "is_published"]
    success_url = reverse_lazy('myblog:post_list')

    def get_success_url(self):
        return reverse('myblog:post_detail', args=[self.kwargs.get('pk')])


class PostDeleteView(DeleteView):
    model = MyPosts
    template_name = 'myblog/post_confirm_delete.html'
    success_url = reverse_lazy('myblog:post_list')




class ContactView(View):
    template_name = 'myblog/contacts.html'

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
        return render(request, "myblog/contact_success.html", context)
