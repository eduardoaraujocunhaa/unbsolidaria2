# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-09 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unbsolidaria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabalho',
            name='descricao',
            field=models.TextField(max_length=140),
        ),
    ]