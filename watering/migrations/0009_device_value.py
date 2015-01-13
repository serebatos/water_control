# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watering', '0008_branch_last_accessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='value',
            field=models.CharField(default=b'N/A', max_length=7),
            preserve_default=True,
        ),
    ]
