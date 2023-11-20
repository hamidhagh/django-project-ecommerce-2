# Generated by Django 4.2.7 on 2023-11-19 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_product_sold_product_total_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='change',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.IntegerField(default=0)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_update', to='home.product')),
                ('product_line', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_line_update', to='home.productline')),
            ],
        ),
    ]
