# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watering', '0009_device_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='t_end_fact',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='branch',
            name='t_end_plan',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
