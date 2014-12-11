# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('listname', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemname', models.CharField(help_text=b'Name shown in checklist', max_length=200, verbose_name=b'Item Name')),
                ('textbox', models.BooleanField(default=False, help_text=b'Optional textbox next to checklist item for additional data', verbose_name=b'Enable Textbox')),
                ('order', models.IntegerField(verbose_name=b'Order in Checklist')),
                ('unit', models.CharField(help_text=b'Only single team: IT/HR admin/Finance/Supervisor', max_length=50, verbose_name=b'Responsible Team')),
            ],
            options={
                'ordering': ('listname', 'unit', 'order', 'itemname'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Checkpoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deadline', models.IntegerField(verbose_name=b'Days before starting date')),
                ('send_alarm', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('deadline',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('ldap_account', models.CharField(max_length=10, blank=True)),
                ('start_date', models.DateField(verbose_name=b'Date')),
                ('confirmed', models.BooleanField(default=False, verbose_name=b'Confirmed/public')),
                ('archived', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('employee_state', models.CharField(default=b'A', max_length=1, choices=[(b'S', b'Summer worker'), (b'P', b'Part-timer'), (b'T', b'Fixed-term'), (b'A', b'Permanent'), (b'E', b'External')])),
                ('location', models.CharField(default=b'U', max_length=1, choices=[(b'U', b'Unknown'), (b'B', b'Berlin'), (b'D', b'Dusseldorf'), (b'H', b'Helsinki'), (b'L', b'Lontoo'), (b'T', b'Tampere')])),
                ('phone', models.CharField(max_length=30, verbose_name=b'Phone number', blank=True)),
                ('email', models.CharField(max_length=150, verbose_name=b'Contact email', blank=True)),
                ('email_notifications', models.BooleanField(default=True)),
                ('supervisor', models.CharField(max_length=50, verbose_name=b"Supervisor's LDAP account", blank=True)),
                ('comments', models.TextField(max_length=1500, verbose_name=b'Info', blank=True)),
                ('listname', models.ForeignKey(to='employee.Checklist')),
            ],
            options={
                'ordering': ('start_date', 'name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmployeeItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.BooleanField(default=False)),
                ('textvalue', models.CharField(max_length=200, null=True, blank=True)),
                ('comment', models.CharField(max_length=200, blank=True)),
                ('checkpoint_fired', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(to='employee.Employee')),
                ('item', models.ForeignKey(to='employee.ChecklistItem')),
                ('listname', models.ForeignKey(to='employee.Checklist')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmployeeItemLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('value', models.BooleanField(default=False)),
                ('textvalue', models.CharField(max_length=200, null=True, blank=True)),
                ('employee', models.ForeignKey(to='employee.Employee')),
                ('item', models.ForeignKey(to='employee.ChecklistItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmployeeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('changes', models.TextField()),
                ('employee', models.ForeignKey(to='employee.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('group', models.CharField(default=b'UN', max_length=2, choices=[(b'IT', b'IT'), (b'HR', b'HR admin'), (b'SU', b'Supervisor'), (b'DH', b'HR'), (b'DA', b'ADMIN'), (b'DS', b'DE Supervisor'), (b'UN', b'Undefined')])),
            ],
            options={
                'ordering': ('username',),
                'verbose_name_plural': 'User permissions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='checkpoint',
            field=models.ForeignKey(blank=True, to='employee.Checkpoint', help_text=b'Optional. Not yet implemented, just skip.', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='item_pair',
            field=models.ForeignKey(blank=True, to='employee.ChecklistItem', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='listname',
            field=models.ForeignKey(to='employee.Checklist'),
            preserve_default=True,
        ),
    ]
