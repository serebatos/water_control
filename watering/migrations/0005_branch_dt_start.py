# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watering', '0004_auto_20141126_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='dt_start',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
