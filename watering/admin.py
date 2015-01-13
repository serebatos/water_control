from django.contrib import admin
from watering.models import Status, Branch
# Register your models here.


class BranchClass(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['descr', 'status', 't_start', 'duration']}),
        ('Week days', {'fields': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'], }),
    ]
    list_display = ('descr','status','t_start','duration','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')


admin.site.register(Branch, BranchClass)
admin.site.register(Status)