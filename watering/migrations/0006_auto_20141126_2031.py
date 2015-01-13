# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watering', '0005_branch_dt_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='dt_start',
        ),
        migrations.AddField(
            model_name='branch',
            name='t_start',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
