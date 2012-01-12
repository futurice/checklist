from django.db import models
import datetime

# Create your models here.
class Checklist(models.Model):
    listname = models.CharField(max_length=200)
    def __unicode__(self):
        return self.listname

class Checkpoint(models.Model):
    deadline = models.IntegerField(verbose_name="Days before starting date")
    send_alarm = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.deadline)

    class Meta:
        ordering = ('deadline',)

class ChecklistItem(models.Model):
    class Meta:
        ordering = ('listname', 'unit','order','itemname')

    listname = models.ForeignKey('Checklist')
    itemname = models.CharField(max_length=200, verbose_name="Item Name", help_text="Name shown in checklist")
    textbox = models.BooleanField(default=False, verbose_name="Enable Textbox", help_text="Optional textbox next to checklist item for additional data")
    order = models.IntegerField(verbose_name="Order in Checklist")
    unit = models.CharField(max_length=50, verbose_name="Responsible Team", help_text="Only single team: IT/HR admin/Finance/Supervisor")
    item_pair = models.ForeignKey('ChecklistItem', null=True, blank=True)
    checkpoint = models.ForeignKey('Checkpoint', null=True, blank=True, help_text="Optional. Not yet implemented, just skip.")

    def __unicode__(self):
        return self.itemname

EMPLOYEE_STATES= (
    ('S', 'Summer worker'),
    ('P', 'Part-timer'),
    ('T', 'Fixed-term'),
    ('A', 'Permanent'),
    ('E', 'External'))

class Employee(models.Model):
    listname = models.ForeignKey('Checklist')
    name = models.CharField(max_length=100)
    ldap_account = models.CharField(max_length=10, blank=True)
    start_date = models.DateField(verbose_name="Date")
    confirmed = models.BooleanField(default=False, verbose_name="Confirmed/public")
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    employee_state = models.CharField(max_length=1, choices=EMPLOYEE_STATES, default='A')
    phone = models.CharField(max_length=30, blank=True, verbose_name="Phone number")
    email = models.CharField(max_length=150, blank=True, verbose_name="Contact email")
    email_notifications = models.BooleanField(default=True)
    supervisor = models.CharField(max_length=50, blank=True, verbose_name="Supervisor's LDAP account")
    comments = models.TextField(max_length=1500, blank=True, verbose_name="Info")

    @property
    def eta(self):
        return (self.start_date - datetime.date.today()).days


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
