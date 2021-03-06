# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2020-10-05 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0021_quran'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quran',
            name='sorat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quran.Sorat'),
        ),
        migrations.AlterField(
            model_name='quran',
            name='verse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quran.Verse'),
        ),
    ]
