# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-20 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0008_auto_20160820_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='politicalparty',
            name='number',
            field=models.IntegerField(default=1, verbose_name='numero'),
            preserve_default=False,
        ),
    ]
