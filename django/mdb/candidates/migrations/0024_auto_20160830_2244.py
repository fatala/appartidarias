# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-31 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0023_auto_20160830_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='budget_1t',
            field=models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Orçamento 1.o turno'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='budget_2t',
            field=models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Orçamento 2.o turno'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='coalition',
            field=models.CharField(max_length=128, verbose_name='Coligação'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='education',
            field=models.CharField(max_length=128, verbose_name='Nível escolaridade'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='job',
            field=models.CharField(max_length=128, verbose_name='Ocupação'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='reelection',
            field=models.BooleanField(default=False, verbose_name='Re-eleição?'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='status',
            field=models.CharField(choices=[('P', 'Pendente'), ('A', 'Aprovado'), ('D', 'Negado')], default='P', max_length=1, verbose_name='Aprovação candidatura Mulheres do Brasil'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Comentário'),
        ),
        migrations.AlterField(
            model_name='politicalparty',
            name='directory_city',
            field=models.TextField(null=True, verbose_name='diretório municipal'),
        ),
        migrations.AlterField(
            model_name='politicalparty',
            name='directory_national',
            field=models.TextField(null=True, verbose_name='diretório nacional'),
        ),
        migrations.AlterField(
            model_name='politicalparty',
            name='directory_state',
            field=models.TextField(null=True, verbose_name='diretório estadual'),
        ),
    ]
