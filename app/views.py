## redirect for url redirection after user submit data
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from .import models 
from django.http import HttpResponse
from django.http.response import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from rest_framework.parsers import JSONParser 

## Import forms
from .forms import ManagedNodeForm, CredentialForm, RuleForm

## auto forms and update - class based views (CBV)
from django.views.generic import TemplateView, CreateView,DetailView, FormView,ListView,UpdateView,DeleteView

## REST API
from rest_framework import viewsets, status
from .serializers import ManagedNodesSerializer, IncidentsSerializer, IncidentsSerializerNew
from .models import ManagedNodes, Incidents, Credentials, Rules

## Refer to https://www.bezkoder.com/django-rest-api
from rest_framework.decorators import api_view

## for json to text converter and wrinting to log file
import json

## ensure login is there using @login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

## paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

## data trunctate for graph
from django.db.models.functions import TruncDay
import pytz
from django_pivot.pivot import pivot
from django_pivot.histogram import histogram

## date
import time
import datetime
from datetime import date,timedelta
from django.utils import timezone

# Create your views here.
def index(request):
  return HttpResponse("This is app")

def home_view(request):
  #home template file
  return render(request,'app/home.html')  

def incident_demo(request):
    incident_list_graph_label = []
    incident_duration = request.GET.get('duration', 7)
    for duration in range(incident_duration,0,-1):
        this_date_difference = (datetime.datetime.now(timezone.utc) - datetime.timedelta(days=duration)).strftime('%Y-%m-%d')
        #this_date = 
        inc_data = models.Incidents.objects.filter(incident_time__contains=this_date_difference).count()
        incident_list_graph_label.append(this_date_difference)
        #pass
    #strftime("%m/%d/%Y, %H:%M:%S")
    this_date = "2022-03-07" #datetime.now()
    time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=1)
    #dweek = now().today() - timedelta(days=7)
    #inc_data = models.Incidents.objects.annotate(incident_times=TruncDay('incident_time',tzinfo=pytz.UTC)).values('incident_time')
    #inc_data = models.Incidents.objects.filter(incident_time__gte=time_threshold)
    inc_data = models.Incidents.objects.filter(incident_time__contains=this_date)
    #inc_data = models.Incidents.objects.all()
    #return analysis_count 
    #inc_data = pivot(Incidents, 'incident_time', 'incident_priority', 'incident_rule')

    return HttpResponse(incident_list_graph_label)
    #return HttpResponse(this_date)


## dashboard with event logs
@login_required
def dashboard_view(request):

    ## declare empty lists
    incident_list_graph_label = []
    incident_list_graph_items_1 = []
    # get the page ID
    incident_duration = request.GET.get('duration', 7)
    for duration in range(incident_duration,0,-1):
        this_date_difference = (datetime.datetime.now(timezone.utc) - datetime.timedelta(days=duration)).strftime('%Y-%m-%d')
        #this_date = 
        inc_data = models.Incidents.objects.filter(incident_time__contains=this_date_difference).count()
        incident_list_graph_label.append(this_date_difference)
        incident_list_graph_items_1.append(inc_data)

    #dweek = now().today() - timedelta(days=7)

    #incident_list_graph_label = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Noday']
    #incident_list_graph_items_1 = [2, 7, 4, 7, 3]

    all_incidents = models.Incidents.objects.all()
    all_incidents_count = all_incidents.count()

    all_managednodes = models.ManagedNodes.objects.all()
    all_managednodes_count = all_managednodes.count()

    all_credentials = models.Credentials.objects.all()
    all_credentials_count = all_credentials.count()

    all_rules = models.Rules.objects.all()
    all_rules_count = all_rules.count()

    context = {'dashboard_data': {
                  'all_incidents_count': all_incidents_count,
                  'all_managednodes_count': all_managednodes_count,
                  'all_credentials_count': all_credentials_count,
                  'all_rules_count': all_rules_count,
                  'incident_list_graph_label': json.dumps(incident_list_graph_label),
                  'incident_list_graph_items_1': json.dumps(incident_list_graph_items_1),
                  }
              }
    return render(request,'app/dashboard.html',context=context) 

## incident list view --> template/app/incidents.html
@login_required
def incident_view(request):
    ## order_by reverse - latest incident on top
    all_incidents = models.Incidents.objects.all().order_by('-incident_time')
  
    # get the page ID
    page = request.GET.get('page', 1)

    paginator = Paginator(all_incidents, 10)
    ##page_range = paginator.get_elided_page_range(number=page)

    try:
        incidents = paginator.page(page)
    except PageNotAnInteger:
        incidents = paginator.page(1)
    except EmptyPage:
        incidents = paginator.page(paginator.num_pages)

    context = {'incidents':incidents}
    return render(request,'app/incidents.html',context=context) 

@login_required
def rules_view(request):
  ## order_by reverse - latest incident on top
  all_rules = models.Rules.objects.all().order_by('rule_name')
  context = {'all_rules':all_rules}
  return render(request,'app/rules.html',context=context) 

# rules create view
class RuleCreateView(LoginRequiredMixin, CreateView):
    model = Rules
    form_class = RuleForm
    success_url = reverse_lazy('app:rules_view')
class RuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Rules
    form_class = RuleForm
    success_url = reverse_lazy('app:rules_view')
    
class RuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Rules
    success_url = reverse_lazy('app:rules_view')

@login_required
def managed_nodes_view(request):
  ## order_by managed nodes
  all_managed_nodes = models.ManagedNodes.objects.all().order_by('instance_name')
  #models.Incidents.objects.all().order_by('-incident_time')
  context = {'all_managed_nodes':all_managed_nodes}
  return render(request,'app/managed_nodes.html',context=context)

## Managed node create view
class ManagedNodeCreateView(LoginRequiredMixin, CreateView):
    # AUTO CONNECTS TO A TEMPLATE WITH THE NAME:
    # model_form.html
    # Make sure to match this template name schema!!
    model = ManagedNodes
    #fields = ['instance_name', 'instance_name_connection','instance_credential']
    #fields = '__all__'
   
    form_class = ManagedNodeForm
    #template_name = 'app/managednodes_form.html'
    success_url = reverse_lazy('app:managed_nodes_view')

class ManagedNodeUpdateView(LoginRequiredMixin, UpdateView):
    # Note! Uses model_form.html file as well
    # same form as CreateView
    model = ManagedNodes
    #fields = "__all__"
    #fields = ['id','instance_name', 'instance_name_connection','instance_credential']
    form_class = ManagedNodeForm
    #template_name = 'app/managednodes_form.html'

    success_url = reverse_lazy('app:managed_nodes_view')

class ManagedNodeDeleteView(LoginRequiredMixin, DeleteView):
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
class CredentialCreateView(LoginRequiredMixin, CreateView):
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
class CredentialUpdateView(LoginRequiredMixin, UpdateView):
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

class CredentialDeleteView(LoginRequiredMixin, DeleteView):
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
        