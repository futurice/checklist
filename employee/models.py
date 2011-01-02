from django.db import models

# Create your models here.
class Checklist(models.Model):
    listname = models.CharField(max_length=200)

class ChecklistItem(models.Model):
    class Meta:
        ordering = ('unit','order','itemname')
    listname = models.ForeignKey('Checklist')
    itemname = models.CharField(max_length=100, verbose_name="Item Name")
    textbox = models.BooleanField(default=False, verbose_name="Enable Textbox")
    order = models.IntegerField(verbose_name="Order in Checklist")
    unit = models.CharField(max_length=50, verbose_name="Responsible Team")
    item_pair = models.ForeignKey('ChecklistItem', null=True)

    def __unicode__(self):
        return self.itemname

class Employee(models.Model):
    listname = models.ForeignKey('Checklist')
    name = models.CharField(max_length=100)
    start_date = models.DateField(verbose_name="Start date")
    confirmed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    supervisor = models.CharField(max_length=50, blank=True, verbose_name="Supervisor's LDAP account")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Phone number")
    email = models.CharField(max_length=150, blank=True, verbose_name="Contact email")
    email_notifications = models.BooleanField(default=True)
    comments = models.TextField(max_length=1500, blank=True, verbose_name="Info")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('start_date', 'name')

class EmployeeItem(models.Model):
    listname = models.ForeignKey('Checklist')
    employee = models.ForeignKey('Employee')
    item = models.ForeignKey('ChecklistItem')
    value = models.BooleanField(default=False)
    textvalue = models.CharField(max_length=200,blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return "%s: %s - %s" % (self.employee.name, self.item.itemname, self.value)
