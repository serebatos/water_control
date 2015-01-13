# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watering', '0002_auto_20141126_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='friday',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='monday',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='saturday',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='sunday',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='thursday',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='tuesday',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='branch',
            name='wednesday',
            field=models.BooleanField(verbose_name=False),
            preserve_default=True,
        ),
    ]
