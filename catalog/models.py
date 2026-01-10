from django.db import models


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

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["product_name", "category"]

    def __str__(self):
        return f"Наименование: {self.product_name}, Цена: {self.price}"
