# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def deduplicate_employeeitems(apps, schema_editor):
    EmployeeItem = apps.get_model('employee', 'EmployeeItem')
    itemForKey = {}
    for item in EmployeeItem.objects.all():
        key = '{}-{}-{}'.format(item.item.id, item.employee.id,
                item.listname.id)
        if key not in itemForKey:
            itemForKey[key] = item
            continue
        if not item.value:
            print('Deleting', item)
            item.delete()
            continue

        old = itemForKey[key]
        print('Deleting', old)
        old.delete()

        itemForKey[key] = item


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_tribe'),
    ]

    operations = [
        migrations.RunPython(deduplicate_employeeitems),
    ]
