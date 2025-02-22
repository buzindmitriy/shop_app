# Generated by Django 5.1.6 on 2025-02-15 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_alter_product_options_product_publication_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_publish",
            field=models.BooleanField(
                default=False, verbose_name="Опубликовать продукт?"
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец продукта",
            ),
        ),
    ]
