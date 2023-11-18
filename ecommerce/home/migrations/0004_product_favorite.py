# Generated by Django 4.2.7 on 2023-11-17 10:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorite',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_favorite', to=settings.AUTH_USER_MODEL),
        ),
    ]