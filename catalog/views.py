from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Product


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
