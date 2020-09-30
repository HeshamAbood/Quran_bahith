# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-09-27 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0004_verse_chars_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verse',
            name='chars_count',
            field=models.TextField(default={' ': 0, 'ء': 1, 'أ': 1, 'ؤ': 6, 'ئ': 1, 'ا': 1, 'ب': 2, 'ة': 400, 'ت': 400, 'ث': 500, 'ج': 3, 'ح': 8, 'خ': 600, 'د': 4, 'ذ': 700, 'ر': 200, 'ز': 7, 'س': 60, 'ش': 300, 'ص': 90, 'ض': 800, 'ط': 9, 'ظ': 900, 'ع': 70, 'غ': 1000, 'ف': 80, 'ق': 100, 'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'ه': 5, 'و': 6, 'ى': 1, 'ي': 10}, max_length=10000, null=True),
        ),
    ]
