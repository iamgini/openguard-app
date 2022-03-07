from django import forms
from django.forms import ModelForm
from .models import ManagedNodes

class ManagedNodeForm(forms.ModelForm):
    class Meta:
      model = ManagedNodes
      fields = "__all__"
      widgets={
        'instance_name' : forms.TextInput(attrs={'class':'form-control'}),
        'instance_credential' : forms.TextInput(attrs={'class':'form-control'})
      }

    #Node name = forms.CharField()
    #Node connection name = forms.CharField()
#
    #def send_email(self):
    #    # send email using the self.cleaned_data dictionary
    #    pass