from django.db import models

from users.models import User


class Category(models.Model):

    category_name = models.CharField(
        max_length=255, verbose_name="Категория", help_text="Введите название категории"
    )
    description = models.TextField(
        verbose_name="Описание категории", blank=True, null=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"Название категории: {self.category_name}"


class Product(models.Model):

    product_name = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
    )
    description = models.TextField(
        verbose_name="Описание продукта", blank=True, null=True
    )
    image = models.ImageField(upload_to="images/", verbose_name="Изображение")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="category",
        null=True,
        blank=True,
    )
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, verbose_name="Владелец продукта", help_text="Укажите владельца продукта", blank=True, null=True, on_delete=models.SET_NULL)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["product_name", "category"]
        permissions = [
            ("can_unpublish_product", "can unpublish product")
        ]

    def __str__(self):
        return f"Наименование: {self.product_name}, Цена: {self.price}"
