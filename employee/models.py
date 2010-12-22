from django.db import models

# Create your models here.
class Checklist(models.Model):
    listname = models.CharField(max_length=200)

class ChecklistItem(models.Model):
    class Meta:
        ordering = ('order','itemname')
    listname = models.ForeignKey('Checklist')
    itemname = models.CharField(max_length=100)
    textbox = models.BooleanField(default=False)
    order = models.IntegerField()
    unit = models.CharField(max_length=50)

class Employee(models.Model):
    listname = models.ForeignKey('Checklist')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    confirmed = models.BooleanField(default=False)

class EmployeeItem(models.Model):
    listname = models.ForeignKey('Checklist')
    employee = models.ForeignKey('employee')
    item = models.ForeignKey('ChecklistItem')
    value = models.BooleanField(default=False)
    textvalue = models.CharField(max_length=200,blank=True,null=True)
