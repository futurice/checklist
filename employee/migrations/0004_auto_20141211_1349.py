# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_deduplicate_employeeitem'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employeeitem',
            unique_together=set([('listname', 'employee', 'item')]),
        ),
    ]
