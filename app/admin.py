from django.contrib import admin

# Register your models here.
from app.models import ManagedNodes

# Register your models here - simple way
admin.site.register(ManagedNodes)

# modify the CarAdmin model
#class ManagedNodesAdmin(admin.ModelAdmin):
#
#    # change the order of fields
#    # fields = ['year','brand']
#    
#    # Using fieldsets
#    # adjust the order of fields and names, category etc
#    fieldsets = [
#        ('TIME INFORMATION', {'fields':['year']}),
#        ('CAR INFORMATION',{'fields':['brand']})
#    ]

#admin.site.register(Car,CarAdmin)