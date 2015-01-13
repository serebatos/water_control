# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watering', '0007_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='last_accessed',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
