# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-06 04:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beer_name', models.CharField(max_length=250)),
                ('beer_type', models.CharField(max_length=20)),
                ('beer_description', models.TextField(default=b'')),
                ('beer_image', models.FileField(default=b'', upload_to=b'')),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brew_name', models.CharField(max_length=50)),
                ('brew_location', models.CharField(max_length=70)),
                ('brew_logo', models.FileField(upload_to=b'')),
                ('is_favorite', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='beer',
            name='brewery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='texasbrew.Brewery'),
        ),
    ]
