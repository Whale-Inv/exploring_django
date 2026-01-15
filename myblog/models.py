from django.db import models



class MyPosts(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", help_text="Введите заголовок")
    content = models.TextField(verbose_name="Содержимое", blank=True, null=True, help_text="Введите содержимое")
    image = models.ImageField(upload_to="myblog/images/", verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", help_text="Дата создания")
    is_published = models.BooleanField(verbose_name="Признак публикации", help_text="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f"Публикация {self.title}, создана{self.created_at}, {self.created_at} просмотров"

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ["created_at"]
