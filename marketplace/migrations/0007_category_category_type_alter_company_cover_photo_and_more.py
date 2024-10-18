# Generated by Django 5.1 on 2024-10-18 13:04

import cloudinary.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_alter_company_cover_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_type',
            field=models.CharField(blank=True, choices=[('EMPRESA', 'Categoría Empresa'), ('SERVICIOS', 'Categoría Servicios'), ('PRODUCTOS', 'Categoría Productos'), ('PAIS', 'Categoría País')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='cover_photo',
            field=cloudinary.models.CloudinaryField(help_text='Foto de portada de la compañía', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='company',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(help_text='Imagen de perfil de la compañía', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=cloudinary.models.CloudinaryField(help_text='Imagen del producto', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='topburgeritem',
            name='custom_url',
            field=models.URLField(blank=True, help_text='URL personalizada para elementos de banner', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='topburgeritem',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(help_text='Imagen destacada de la hamburguesa', max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='topburgeritem',
            name='order',
            field=models.IntegerField(help_text='Posición en el top (1-3)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AlterField(
            model_name='topburgersection',
            name='position',
            field=models.IntegerField(default=0, help_text='Orden de posición para mostrar secciones'),
        ),
    ]
