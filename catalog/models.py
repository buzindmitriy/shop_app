from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Категория")
    description = models.TextField(blank=True, verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Продукт")
    description = models.TextField(verbose_name="Описание продукта")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="Продукты"
    )
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение", blank=True, null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата изменения")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец продукта", null=True,
                              blank=True)
    is_publish = models.BooleanField(default=False, verbose_name="Опубликовать продукт?")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = [
            ('can_unpublish_product', 'Can unpublished product'),
            ('can_delete_product', 'Can delete product'),
        ]

    def __str__(self):
        return self.name
