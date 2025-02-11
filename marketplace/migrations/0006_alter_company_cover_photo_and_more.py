# Generated by Django 5.1 on 2024-10-17 19:52

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_alter_topburgersection_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cover_photo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='company',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='topburgeritem',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(help_text='Featured burger image', max_length=255, verbose_name='image'),
        ),
    ]
