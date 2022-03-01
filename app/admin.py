from django.contrib import admin

# Register your models here.
from app.models import ManagedNodes,Credentials

# Customize admin portal
admin.site.site_header = 'OpenGuard Admin Dashboard'
admin.site.site_title = 'OpenGuard Admin'
admin.site.index_title = 'Dashboard'
#admin.site.site_url = "Url for view site button"

# Register your models here - simple way
#admin.site.register(ManagedNodes)

# modify the ManagedNodes model
class ManagedNodesAdmin(admin.ModelAdmin):
    # Using fieldsets
    # adjust the order of fields and names, category etc
    fieldsets = [
        ('Managed Node', {'fields':['instance_name', 'instance_name_connection']}),
        ('Connection', {'fields':['instance_credential']}),
    ]
class CredentialsAdmin(admin.ModelAdmin):
    # Using fieldsets
    # adjust the order of fields and names, category etc
    fieldsets = [
        ('Credential', {'fields':['cred_name', 'cred_type']}),
        ('Secret', {'fields':['cred_ssh_private_key']}),
    ]

admin.site.register(ManagedNodes,ManagedNodesAdmin)
admin.site.register(Credentials,CredentialsAdmin)