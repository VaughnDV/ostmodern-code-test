# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-04 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shiptrader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='starship',
            name='cargo_capacity',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='starship',
            name='crew',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='starship',
            name='hyperdrive_rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='starship',
            name='length',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='starship',
            name='passengers',
            field=models.IntegerField(null=True),
        ),
    ]
