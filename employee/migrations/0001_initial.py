# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Checklist'
        db.create_table('employee_checklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listname', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('employee', ['Checklist'])

        # Adding model 'Checkpoint'
        db.create_table('employee_checkpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deadline', self.gf('django.db.models.fields.IntegerField')()),
            ('send_alarm', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('employee', ['Checkpoint'])

        # Adding model 'ChecklistItem'
        db.create_table('employee_checklistitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employee.Checklist'])),
            ('itemname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('textbox', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('item_pair', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employee.ChecklistItem'], null=True, blank=True)),
            ('checkpoint', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employee.Checkpoint'], null=True, blank=True)),
        ))
        db.send_create_signal('employee', ['ChecklistItem'])

        # Adding model 'Employee'
        db.create_table('employee_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employee.Checklist'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('email_notifications', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('supervisor', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=1500, blank=True)),
        ))
        db.send_create_signal('employee', ['Employee'])

        # Adding model 'EmployeeItem'
        db.create_table('employee_employeeitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listname', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employee.Checklist'])),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employee.Employee'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employee.ChecklistItem'])),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('textvalue', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('checkpoint_fired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('employee', ['EmployeeItem'])


    def backwards(self, orm):
        
        # Deleting model 'Checklist'
        db.delete_table('employee_checklist')

        # Deleting model 'Checkpoint'
        db.delete_table('employee_checkpoint')

        # Deleting model 'ChecklistItem'
        db.delete_table('employee_checklistitem')

        # Deleting model 'Employee'
        db.delete_table('employee_employee')

        # Deleting model 'EmployeeItem'
        db.delete_table('employee_employeeitem')


    models = {
        'employee.checklist': {
            'Meta': {'object_name': 'Checklist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listname': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'employee.checklistitem': {
            'Meta': {'ordering': "('listname', 'unit', 'order', 'itemname')", 'object_name': 'ChecklistItem'},
            'checkpoint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Checkpoint']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_pair': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.ChecklistItem']", 'null': 'True', 'blank': 'True'}),
            'itemname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'listname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Checklist']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'textbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'employee.checkpoint': {
            'Meta': {'ordering': "('deadline',)", 'object_name': 'Checkpoint'},
            'deadline': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_alarm': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'employee.employee': {
            'Meta': {'ordering': "('start_date', 'name')", 'object_name': 'Employee'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '1500', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Checklist']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'supervisor': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'employee.employeeitem': {
            'Meta': {'object_name': 'EmployeeItem'},
            'checkpoint_fired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.ChecklistItem']"}),
            'listname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Checklist']"}),
            'textvalue': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['employee']
