# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserPermissions'
        db.create_table('employee_userpermissions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('group', self.gf('django.db.models.fields.CharField')(default='UN', max_length=2)),
        ))
        db.send_create_signal('employee', ['UserPermissions'])


    def backwards(self, orm):
        
        # Deleting model 'UserPermissions'
        db.delete_table('employee_userpermissions')


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
            'itemname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'ldap_account': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'listname': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Checklist']"}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
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
        },
        'employee.employeeitemlog': {
            'Meta': {'object_name': 'EmployeeItemLog'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.ChecklistItem']"}),
            'textvalue': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'employee.employeelog': {
            'Meta': {'object_name': 'EmployeeLog'},
            'changes': ('django.db.models.fields.TextField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'employee.userpermissions': {
            'Meta': {'object_name': 'UserPermissions'},
            'group': ('django.db.models.fields.CharField', [], {'default': "'UN'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['employee']
