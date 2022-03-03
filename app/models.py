from datetime import datetime
from django.utils import timezone
from django.db import models
# Create your models here.
class ManagedNodes(models.Model):
  instance_name = models.CharField(max_length=50)
  instance_name_connection = models.CharField(max_length=50)
  instance_credential = models.CharField(max_length=50)
  date_time = models.DateTimeField(default=timezone.now)
  def __str__(self):
    return f"{ self.instance_name} connects using {self.instance_credential}"

class Credentials(models.Model):
  cred_name = models.CharField(max_length=20)
  cred_type = models.CharField(max_length=50)
  cred_ssh_private_key = models.CharField(default=' ', max_length=5000)

  def __str__(self):
    return f"{ self.cred_name} connects using {self.cred_type}"
    
# incident logs 
class Incidents(models.Model):
  incident_time_reported = models.DateTimeField(auto_now=True)
  incident_time = models.DateTimeField()
  incident_priority = models.CharField(max_length=10, default='')
  incident_rule = models.CharField(max_length=25, default='')
  incident_output = models.CharField(max_length=100, default='')
  incident_output_fields = models.CharField(max_length=1000, default='')

  def __str__(self):
    return f"{ self.incident_time} connects using {self.incident_output}"
        