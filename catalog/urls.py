from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, product_list, product_detail, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path("", product_list, name="products_list"),
    path("catalog/<int:pk>/", product_detail, name="product_detail"),
    path('add/', add_product, name='add_product'),
    path("contacts/", contacts, name="contacts"),
]
