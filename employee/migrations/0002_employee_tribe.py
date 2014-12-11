# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='tribe',
            field=models.CharField(default='', max_length=50, verbose_name=b'Tribe', blank=True),
            preserve_default=False,
        ),
    ]
