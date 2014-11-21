# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Employee.employee_state'
        db.add_column('employee_employee', 'employee_state', self.gf('django.db.models.fields.CharField')(default='A', max_length=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Employee.employee_state'
        db.delete_column('employee_employee', 'employee_state')


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
            'employee_state': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
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
