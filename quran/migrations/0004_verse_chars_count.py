# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-09-27 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0003_auto_20200926_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='verse',
            name='chars_count',
            field=models.TextField(default=models.TextField(max_length=10000), max_length=10000, null=True),
        ),
    ]
