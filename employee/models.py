from django.db import models

# Create your models here.
class Checklist(models.Model):
    listname = models.CharField(max_length=200)
    def __unicode__(self):
        return self.listname

class Checkpoint(models.Model):
    deadline = models.IntegerField(verbose_name="Days before starting date")
    send_alarm = models.BooleanField(default=True)

class ChecklistItem(models.Model):
    class Meta:
        ordering = ('unit','order','itemname')
    listname = models.ForeignKey('Checklist')
    itemname = models.CharField(max_length=100, verbose_name="Item Name")
    textbox = models.BooleanField(default=False, verbose_name="Enable Textbox")
    order = models.IntegerField(verbose_name="Order in Checklist")
    unit = models.CharField(max_length=50, verbose_name="Responsible Team")
    item_pair = models.ForeignKey('ChecklistItem', null=True, blank=True)
    checkpoint = models.ForeignKey('Checkpoint', null=True, blank=True)

    def __unicode__(self):
        return self.itemname

class Employee(models.Model):
    listname = models.ForeignKey('Checklist')
    name = models.CharField(max_length=100)
    start_date = models.DateField(verbose_name="Date")
    confirmed = models.BooleanField(default=False, verbose_name="Confirmed/public")
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    phone = models.CharField(max_length=30, blank=True, verbose_name="Phone number")
    email = models.CharField(max_length=150, blank=True, verbose_name="Contact email")
    email_notifications = models.BooleanField(default=True)
    supervisor = models.CharField(max_length=50, blank=True, verbose_name="Supervisor's LDAP account")
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
    checkpoint_fired = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s - %s" % (self.employee.name, self.item.itemname, self.value)
