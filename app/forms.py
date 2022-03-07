#from django import forms
#from django.forms import ModelForm
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit
#from .models import ManagedNodes

#class ManagedNodeForm(forms.ModelForm):
#    class Meta:
#      model = ManagedNodes
#      #fields = "__all__"
#      fields = ['instance_name',
#                'instance_name_connection',#'instance_credential']
#      def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_method = 'post'
#        #self.helper.form_tag = False
#        self.helper.add_input(Submit('submit', 'Save Node'))