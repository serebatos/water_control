from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=15)
    descr = models.CharField(max_length=30)
    value = models.CharField(max_length=7, default='N/A')

    def __str__(self):
        return self.descr

    def get_absolute_url(self):
        return reverse('temp-detail', kwargs={'pk': self.pk})

# todo: Creation of default values for statuses
class Status(models.Model):
    name = models.CharField(max_length=15)
    descr = models.CharField(max_length=30)

    def __str__(self):
        return self.descr


class Branch(models.Model):
    descr = models.CharField(max_length=30)
    status = models.ForeignKey(Status)
    t_start_plan = models.TimeField(null=True, blank=True)
    t_start_fact = models.TimeField(null=True, blank=True)
    # equals t_start + duration and must be set when start and be clean up when finish
    t_end_plan = models.TimeField(null=True, blank=True)
    # must be set when real stop occurs
    t_end_fact = models.TimeField(null=True, blank=True)

    # in minutes
    duration = models.IntegerField(default=30)

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    last_accessed = models.DateTimeField(null=True)

    def __str__(self):
        return self.descr

    def get_absolute_url(self):
        return reverse('branch-detail', kwargs={'pk': self.pk})



