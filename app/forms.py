from django import forms
from django.forms import ModelForm
#from django.forms import ModelForm
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
from .models import ManagedNodes, Credentials, Rules, Tokens

## for random token value
import random
import string

## random generator
def token_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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

      #fields = "__all__"
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
      widgets = {
            #'cred_ssh_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'please enter password'}),
            'cred_ssh_password': forms.PasswordInput(render_value=True,attrs={'class': 'form-control',}),
            #'cred_ssh_private_key': forms.PasswordInput(render_value=True,attrs={'class': 'form-control',}),
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

class RuleForm(forms.ModelForm):
    class Meta:
      model = Rules
#      #fields = "__all__"
      fields = ('rule_name',
                'rule_fix_playbook',
                )
      labels = {
            'rule_name': ('Rule name'),
            'rule_fix_playbook': ('Name of playbook to execute'),
          }
      help_texts = {
            'rule_name': ('Use "FALCO_OGRULE_" as prefix to identify.'),
            'rule_fix_playbook': ('This Ansible playbook will be used to remediate the violation of the rule.'),
        }
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
        self.fields['rule_name'].initial = "FALCO_OGRULE_"
        #self.fields['instance_credential'].queryset = Credentials.objects.none()
        #CREDENTIAL_TYPES= [
        #  ('Username-Password', 'Username-Password'),
        #  ('SSH-Key', 'SSH-Key'),
        #  ]
        #credential_choices = [(str(cred.id) + '_' + cred.cred_name, str(cred.id) + '_' + cred.cred_name) for cred in Credentials.objects.all().order_by('pk')]
        #self.fields['cred_type'].choices = CREDENTIAL_TYPES

    #cred_type = forms.ChoiceField()    

class TokenForm(forms.ModelForm):
    class Meta:
      model = Tokens
#      #fields = "__all__"
      fields = ('token_name',
                'token_desc',
                'token_value'
                )
      labels = {
            'token_name': ('Token name'),
            'token_desc': ('Description for the Token'),
            'token_value': ("Access Token"),
          }
      help_texts = {
            #'token_name': ('Use "FALCO_OGRULE_" as prefix to identify.'),
            #'token_value': ('This Ansible playbook will be used to remediate the violation of the rule.'),
            'token_desc': ('Eg: Token for connecting from a falco agent'),
            'token_value': ("Auto generated value; please save this as the token will not be displayed again !"),
        }
      widgets = {
            #'cred_ssh_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'please enter password'}),
            #'token_value': forms.TextInput(attrs={'disabled': True}),
            'token_value': forms.TextInput(attrs={'class': 'form-control',}),
            #'cred_ssh_private_key': forms.PasswordInput(render_value=True,attrs={'class': 'form-control',}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_token = token_generator()
        self.fields['token_value'].initial = new_token
