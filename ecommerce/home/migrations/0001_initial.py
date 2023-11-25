# Generated by Django 4.2.7 on 2023-11-25 13:53

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub', to='home.category')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gallary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, upload_to='gallary/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('amount', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('chart_change', models.BooleanField(default=False)),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='product')),
                ('status', models.CharField(blank=True, choices=[('None', 'none'), ('size', 'size'), ('color', 'color'), ('both', 'both')], max_length=255, null=True)),
                ('available', models.BooleanField(default=True)),
                ('total_favorite', models.IntegerField(default=0)),
                ('sold', models.IntegerField(default=0)),
                ('change', models.BooleanField(default=False)),
                ('total_view', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.category')),
                ('color', models.ManyToManyField(blank=True, to='home.color')),
                ('dislike', models.ManyToManyField(blank=True, related_name='product_dislike', to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(blank=True, related_name='user_favorite', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, related_name='product_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=200, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_view', to='home.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('amount', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('chart_change', models.BooleanField(default=False)),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.size')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='image/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, to='home.size'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='product',
            name='view',
            field=models.ManyToManyField(blank=True, related_name='product_view', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Compare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=100, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rate', models.PositiveIntegerField(default=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('is_reply', models.BooleanField(default=False)),
                ('like', models.ManyToManyField(blank=True, related_name='comment_like', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reply', to='home.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
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
