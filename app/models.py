from django.db import models
# Create your models here.
class ManagedNodes(models.Model):
  instance_name = models.CharField(max_length=50)
  instance_name_connection = models.CharField(max_length=50)
  instance_credential = models.CharField(max_length=50)

  def __str__(self):
    return f"{ self.instance_name} connects using {self.instance_credential}"

class Credentials(models.Model):
  instance_name = models.CharField(max_length=50)
  instance_name_connection = models.CharField(max_length=50)
  instance_credential = models.CharField(max_length=50)

  def __str__(self):
    return f"{ self.instance_name} connects using {self.instance_credential}"