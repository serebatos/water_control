from django.contrib import admin
from watering.models import Status, Branch, Maintanence
# Register your models here.


class BranchClass(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['leg', 'descr', 'status', 't_start_plan', 'duration']}),
        ('Week days', {'fields': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'], }),
    ]
    list_display = (
        'leg', 'descr', 'status', 't_start_plan', 'duration', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
        'saturday', 'sunday')


admin.site.register(Branch, BranchClass)
admin.site.register(Status)
admin.site.register(Maintanence)