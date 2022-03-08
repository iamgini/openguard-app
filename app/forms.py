from django import forms
from django.forms import ModelForm
#from django.forms import ModelForm
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
from .models import ManagedNodes, Credentials
from .models import Credentials

class ManagedNodeForm(forms.ModelForm):
    class Meta:
      model = ManagedNodes
#      #fields = "__all__"
      fields = ('instance_name',
                'instance_name_connection',
                'instance_credential')
      labels = {
            'instance_name': ('Managed node'),
            'instance_name_connection': ('Connection name(IP Address or FQDN))'),
            'instance_credential': ('Credential to use for accessing the node')
        }
      help_texts = {
            'instance_name': ('Enter the Managed node information.'),
            'instance_credential': ('Make sure the managed node is able to access from this system using this credential.'),
        }
      #error_messages = {
      #      'name': {
      #          'max_length': _("This writer's name is too long."),
      #      },
      #  }

      widgets = {
            #'instance_credential': forms.Select(attrs={'class': 'form-control'}),
            'instance_credential': forms.Select(attrs={'class': 'form-control'}),
        }
        #'instance_credential': forms.Select(choices=CREDENTIAL_CHOICES,attrs={'class': 'form-control'}),
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instance_name'].initial = ""
        #self.fields['instance_credential'].initial = "Hi"
        #self.fields['instance_credential'].initial = "Hi"
        #self.fields['instance_credential'].queryset = Credentials.objects.none()

        credential_choices = [(str(cred.id) + '_' + cred.cred_name, str(cred.id) + '_' + cred.cred_name) for cred in Credentials.objects.all().order_by('pk')]
        self.fields['instance_credential'].choices = credential_choices

    instance_credential = forms.ChoiceField()

#      def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_method = 'post'
#        #self.helper.form_tag = False
#        self.helper.add_input(Submit('submit', 'Save Node'))

class CredentialForm(forms.ModelForm):
    class Meta:
      model = Credentials
#      #fields = "__all__"
      fields = ('cred_name',
                'cred_type',
                'cred_ssh_user_name',
                'cred_ssh_password',
                'cred_ssh_private_key')
      labels = {
            'cred_name': ('Credential name'),
            'cred_type': ('Type of credential'),
            'cred_ssh_user_name': ('SSH Username (if Username-Password credential)'),
            'cred_ssh_password': ('SSH Password (if Username-Password credential)'),
            'cred_ssh_private_key': ('SSH private key (if SSH-Key credential)'),
        }
      #help_texts = {
      #      'instance_name': ('Enter the Managed node information.'),
      #      'instance_credential': ('Make sure the managed node is able to access from this system using this credential.'),
      #  }
      #error_messages = {
      #      'name': {
      #          'max_length': _("This writer's name is too long."),
      #      },
      #  }

      #widgets = {
      #      #'instance_credential': forms.Select(attrs={'class': 'form-control'}),
      #      'instance_credential': forms.Select(attrs={'class': 'form-control'}),
      #  }
      #  #'instance_credential': forms.Select(choices=CREDENTIAL_CHOICES,attrs={'class': 'form-control'}),
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['instance_name'].initial = ""
        #self.fields['instance_credential'].initial = "Hi"
        #self.fields['instance_credential'].initial = "Hi"
        #self.fields['instance_credential'].queryset = Credentials.objects.none()
        CREDENTIAL_TYPES= [
          ('Username-Password', 'Username-Password'),
          ('SSH-Key', 'SSH-Key'),
          ]
        #credential_choices = [(str(cred.id) + '_' + cred.cred_name, str(cred.id) + '_' + cred.cred_name) for cred in Credentials.objects.all().order_by('pk')]
        self.fields['cred_type'].choices = CREDENTIAL_TYPES

    cred_type = forms.ChoiceField()