# Generated by Django 5.1.6 on 2025-02-10 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="token",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="token"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="users/avatars/"),
        ),
        migrations.AlterField(
            model_name="user",
            name="country",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
