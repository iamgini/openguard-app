from datetime import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
class ManagedNodes(models.Model):
  instance_name = models.CharField(max_length=50)
  instance_name_connection = models.CharField(max_length=50)
  instance_credential = models.CharField(max_length=50)
  #instance_credential_to_use = models.CharField(max_length=50,default='Username-Password')
  date_time = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f"{ self.instance_name} connects using {self.instance_credential}"

  def details(self):
    return repr( dict( instance_name=self.instance_name, instance_name_connection=self.instance_name_connection, instance_credential=self.instance_credential, date_time=self.date_time ) )

  ## source a model field into another model django
  ## https://www.codegrepper.com/code-examples/python/source+a+model+field+into+another+model+django
  #def save(self, *args, **kwargs):
  #  self.instance_credential = self.instance_credential + 'SSH'
  #  super(ManagedNodes, self).save(*args, **kwargs)

## Check Rules and playbook
class Rules(models.Model):
  rule_name = models.CharField(max_length=50)
  rule_fix_playbook = models.CharField(max_length=50)

class Credentials(models.Model):
  cred_name = models.CharField(max_length=20)
  cred_type = models.CharField(max_length=50)
  cred_ssh_user_name = models.CharField(default=' ', max_length=100)
  cred_ssh_password = models.CharField(default=' ', max_length=100)
  cred_ssh_private_key = models.CharField(default=' ', max_length=5000)

  def __str__(self):
    return f"{self.cred_name}"
    
# incident logs 
class Incidents(models.Model):
  incident_time_reported = models.DateTimeField(auto_now=True)
  incident_time = models.DateTimeField()
  incident_priority = models.CharField(max_length=10, default='')
  incident_rule = models.CharField(max_length=300, default='')
  incident_output = models.CharField(max_length=2000, default='')
  incident_hostname = models.CharField(max_length=1000, default='')

  ## for incident status  - fixed, pending etc.
  incident_status = models.CharField(max_length=100, default='PENDING')
  incident_time_fixed = models.DateTimeField(auto_now=True)
  incident_fix_comments = models.CharField(max_length=1000, default='')
  #incident_output_fields = models.CharField(max_length=1000, default='')
  #incident_output_fields_new = models.JSONField(default=dict)

  def __str__(self):
    return f"{ self.incident_time} connects using {self.incident_output}"

  def details(self):
    return repr( dict( incident_time_reported=self.incident_time_reported, incident_time=self.incident_time, incident_priority=self.incident_priority, incident_rule=self.incident_rule, incident_output=self.incident_output, incident_hostname=self.incident_hostname ) )
    #return f"{ self.incident_time} connects using {self.incident_output}" 
