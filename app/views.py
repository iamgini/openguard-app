## redirect for url redirection after user submit data
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from .import models 
from django.http import HttpResponse
from django.http.response import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from rest_framework.parsers import JSONParser 

## Import forms
from .forms import ManagedNodeForm, CredentialForm

## auto forms and update
from django.views.generic import TemplateView, CreateView,DetailView, FormView,ListView,UpdateView,DeleteView

## REST API
from rest_framework import viewsets, status
from .serializers import ManagedNodesSerializer, IncidentsSerializer, IncidentsSerializerNew
from .models import ManagedNodes, Incidents, Credentials

## Refer to https://www.bezkoder.com/django-rest-api
from rest_framework.decorators import api_view

## for json to text converter and wrinting to log file
import json

# Create your views here.
def index(request):
  return HttpResponse("This is app")

def home_view(request):
  #home template file
  return render(request,'app/home.html')  

## dashboard with event logs
def dashboard_view(request):
  #home template file
  all_incidents = models.Incidents.objects.all()
  context = {'all_incidents':all_incidents}
  return render(request,'app/dashboard.html',context=context) 

## incident list view --> template/app/incidents.html
def incident_view(request):
  ## order_by reverse - latest incident on top
  all_incidents = models.Incidents.objects.all().order_by('-incident_time')

  context = {'all_incidents':all_incidents}
  return render(request,'app/incidents.html',context=context) 


## incident list view --> template/app/managed_nodes.html
def managed_nodes_view(request):
  ## order_by managed nodes
  all_managed_nodes = models.ManagedNodes.objects.all().order_by('instance_name')
  #models.Incidents.objects.all().order_by('-incident_time')
  context = {'all_managed_nodes':all_managed_nodes}
  return render(request,'app/managed_nodes.html',context=context)

## Managed node create view
class ManagedNodeCreateView(CreateView):
    # AUTO CONNECTS TO A TEMPLATE WITH THE NAME:
    # model_form.html
    # Make sure to match this template name schema!!
    model = ManagedNodes
    #fields = ['instance_name', 'instance_name_connection','instance_credential']
    #fields = '__all__'
   
    form_class = ManagedNodeForm
    #template_name = 'app/managednodes_form.html'
    success_url = reverse_lazy('app:managed_nodes_view')

class ManagedNodeUpdateView(UpdateView):
    # Note! Uses model_form.html file as well
    # same form as CreateView
    model = ManagedNodes
    #fields = "__all__"
    #fields = ['id','instance_name', 'instance_name_connection','instance_credential']
    form_class = ManagedNodeForm
    #template_name = 'app/managednodes_form.html'

    success_url = reverse_lazy('app:managed_nodes_view')

class ManagedNodeDeleteView(DeleteView):
    # Requires model_confirm_delete.html template name
    model = ManagedNodes
    success_url = reverse_lazy('app:managed_nodes_view')

## for fetching credential list
## https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
def load_credentials(request):
    #credential_id = request.GET.get('credential')
    all_credentials = models.Credentials.objects.all().order_by('pk')
    context = {'all_credentials':all_credentials}
    return render(request, 'app/credentials_dropdown_list_options.html', context=context)

## credential list view --> template/app/credentials.html
def credentials_view(request):
    ## order_by managed nodes
    all_credentials = models.Credentials.objects.all().order_by('cred_name')
    #models.Incidents.objects.all().order_by('-incident_time')
    context = {'all_credentials':all_credentials}
    return render(request,'app/credentials.html',context=context)
    
# credential create view
class CredentialCreateView(CreateView):
    model = Credentials
    #fields = ['cred_name', 
    #          'cred_type',
    #          'cred_ssh_user_name',
    #          'cred_ssh_password',
    #          'cred_ssh_private_key']
    #fields = '__all__'
   
    form_class = CredentialForm
    #template_name = 'app/managednodes_form.html'
    success_url = reverse_lazy('app:credentials_view')

# credential create view
class CredentialUpdateView(UpdateView):
    model = Credentials
    #fields = ['cred_name', 
    #          'cred_type',
    #          'cred_ssh_user_name',
    #          'cred_ssh_password',
    #          'cred_ssh_private_key']
    ##fields = '__all__'
   
    form_class = CredentialForm
    #template_name = 'app/managednodes_form.html'
    success_url = reverse_lazy('app:credentials_view')

class CredentialDeleteView(DeleteView):
    # Requires model_confirm_delete.html template name
    model = Credentials
    success_url = reverse_lazy('app:credentials_view')

## Rest API View 
class ManagedNodesViewSet(viewsets.ModelViewSet):
    queryset = ManagedNodes.objects.all().order_by('id')
    serializer_class = ManagedNodesSerializer

## Rest API View 
class IncidentsViewSet(viewsets.ModelViewSet):
    queryset = Incidents.objects.all().order_by('id')
    serializer_class = IncidentsSerializer

## API View
@api_view(['GET', 'POST', 'DELETE'])
def nodes_list(request):
    if request.method == 'GET':
        managenodes = ManagedNodes.objects.all()
        
        node = request.query_params.get('instance_name', None)
        if node is not None:
            managenodes = managenodes.filter(title__icontains=node)
        
        managenodes_serializer = ManagedNodesSerializer(managenodes, many=True)
        return JsonResponse(managenodes_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        managenodes_data = JSONParser().parse(request)
        managenodes_serializer = ManagedNodesSerializer(data=managenodes_data)
        if managenodes_serializer.is_valid():
            managenodes_serializer.save()
            return JsonResponse(managenodes_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(managenodes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #elif request.method == 'DELETE':
    #    count = Tutorial.objects.all().delete()
    #    return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
  
@api_view(['GET', 'POST', 'DELETE'])
def incident_report(request):
    #if request.method == 'GET':
    #    managenodes = ManagedNodes.objects.all()
    #    
    #    node = request.query_params.get('instance_name', None)
    #    if node is not None:
    #        managenodes = managenodes.filter(title__icontains=node)
    #    
    #    managenodes_serializer = ManagedNodesSerializer(managenodes, #many=True)
    #    return JsonResponse(managenodes_serializer.data, safe=False)
    #    # 'safe=False' for objects serialization
    #elif request.method == 'POST':
    if request.method == 'POST':
        incident_data = JSONParser().parse(request)

        incident_serializer = IncidentsSerializerNew(data=incident_data, context={
           "incident_hostname": request.query_params.get("source_hostname")
        })

        my_incident_hostname = request.query_params.get("source_hostname")
        #new_log = open( 'application_logs/logs', "a")
        #new_log.write('\n' + my_incident_hostname + json.dumps( incident_data ))
        #new_log.close()
        if '.ansible/tmp/ansible-tmp' in incident_data['output']:
            if incident_serializer.is_valid():
                #incident_serializer.save    (incident_hostname=my_incident_hostname)
                return JsonResponse(incident_serializer.data,   status=status.HTTP_204_NO_CONTENT) 
            return JsonResponse(incident_serializer.errors,     status=status.HTTP_400_BAD_REQUEST)
            #return incident_data
        else:
            if incident_serializer.is_valid():
                incident_serializer.save    (incident_hostname=my_incident_hostname)
                return JsonResponse(incident_serializer.data,   status=status.HTTP_201_CREATED) 
            return JsonResponse(incident_serializer.errors,     status=status.HTTP_400_BAD_REQUEST)
            #return incident_data
        