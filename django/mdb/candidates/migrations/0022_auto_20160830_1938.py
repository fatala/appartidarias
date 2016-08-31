# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-31 00:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0021_auto_20160822_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('name', models.CharField(max_length=128, verbose_name='Nome')),
                ('comment', models.TextField(blank=True, verbose_name='Comentário')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='criado em')),
                ('approved', models.BooleanField(default=False, verbose_name='aprovado')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidates.Candidate', verbose_name='Candidata')),
            ],
            options={
                'verbose_name_plural': 'Comentários',
                'verbose_name': 'Comentário',
            },
        ),
        migrations.RemoveField(
            model_name='comments',
            name='candidate',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
    ]