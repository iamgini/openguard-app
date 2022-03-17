## redirect for url redirection after user submit data
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from .import models 
from django.http import HttpResponse
from django.http.response import Http404, HttpResponse, HttpResponseNotFound, JsonResponse

## Import forms
from .forms import ManagedNodeForm, CredentialForm, RuleForm, TokenForm

## auto forms and update - class based views (CBV)
from django.views.generic import TemplateView, CreateView,DetailView, FormView,ListView,UpdateView,DeleteView

## for fix jobs to run cron calls
from .cron import my_cron_job

## REST API
from rest_framework import viewsets, status
from .serializers import ManagedNodesSerializer, IncidentsSerializer, IncidentsSerializerNew
from .models import ManagedNodes, Incidents, Credentials, Rules, Tokens

from rest_framework.parsers import JSONParser 
from rest_framework.views import APIView
from rest_framework.response import Response

## REST API Token
from rest_framework.permissions import IsAuthenticated
## https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html

## Refer to https://www.bezkoder.com/django-rest-api
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

## for json to text converter and wrinting to log file
import json

## ensure login is there using @login_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

## paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

## data trunctate for graph
#from django.db.models.functions import TruncDay
#import pytz
#from django_pivot.pivot import pivot
#from django_pivot.histogram import histogram

## date
import time
import datetime
#from datetime import datetime 
from datetime import date,timedelta
#from datetime import datetime,date,timedelta
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

## for cron jobs
def run_fix_jobs(request):
    time_now = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    job_out = my_cron_job()
    return HttpResponse( str(time_now) + ': Jobs checked')

## dashboard with event logs
@login_required
def dashboard_view(request):
    ## declare empty lists
    incident_list_graph_label = []
    incident_list_graph_items_1 = []
    incident_list_graph_items_fixed = []

    incident_status_graph_label = []
    incident_status_graph_item = []
    # get the page ID
    incident_duration = request.GET.get('duration', 30)

    for duration in range(incident_duration,-1,-1):
        this_date_difference = (datetime.datetime.now(timezone.utc) - datetime.timedelta( days=duration )).strftime('%Y-%m-%d')
        this_date_difference_label = (datetime.datetime.now(timezone.utc) - datetime.timedelta(days=duration)).strftime('%m/%d')
        #this_date = 
        inc_data = models.Incidents.objects.filter(incident_time__contains=this_date_difference).count()
        #inc_data_fixed = models.Incidents.objects.filter(incident_time__contains=this_date_difference, incident_status='FIXED').count()
        
        incident_list_graph_label.append(this_date_difference_label)
        incident_list_graph_items_1.append(inc_data)
        #incident_list_graph_items_fixed.append(inc_data)

    #dweek = now().today() - timedelta(days=7)

    #incident_list_graph_label = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Noday']
    #incident_list_graph_items_1 = [2, 7, 4, 7, 3]

    this_date_difference = (datetime.datetime.now(timezone.utc) - datetime.timedelta(days=incident_duration)).strftime('%Y-%m-%d')
    latest_incidents = models.Incidents.objects.all().filter(incident_time__gte=this_date_difference).order_by('-incident_time')[0:5]

    incident_status_list = ["FIXED", "PENDING", "NO_RULE_FOUND"]
    for istatus in incident_status_list:
        incident_status_graph_label.append(istatus)
        incidents_status_count = models.Incidents.objects.all().filter(incident_time__gte=this_date_difference, incident_status=istatus).count()
        incident_status_graph_item.append(incidents_status_count)
    #incidents_fixed = models.Incidents.objects.all().filter(incident_time__gte=this_date_difference, incident_status='FIXED')
    #incidents_pending = models.Incidents.objects.all().filter(incident_time__gte=this_date_difference, incident_status='FIXED')

    all_incidents = models.Incidents.objects.all()
    all_incidents_count = all_incidents.count()

    all_managednodes = models.ManagedNodes.objects.all()
    all_managednodes_count = all_managednodes.count()

    all_credentials = models.Credentials.objects.all()
    all_credentials_count = all_credentials.count()

    all_rules = models.Rules.objects.all()
    all_rules_count = all_rules.count()

    context = {'dashboard_data': {
                  'latest_incidents': latest_incidents,
                  'all_incidents_count': all_incidents_count,
                  'incident_duration': incident_duration,
                  'all_managednodes_count': all_managednodes_count,
                  'all_credentials_count': all_credentials_count,
                  'all_rules_count': all_rules_count,
                  'incident_list_graph_label': json.dumps(incident_list_graph_label),
                  'incident_list_graph_items_1': json.dumps(incident_list_graph_items_1),
                  'incident_status_graph_label': json.dumps(incident_status_graph_label),
                  'incident_status_graph_item': json.dumps(incident_status_graph_item),
                  #'incident_list_graph_items_fixed': json.dumps(incident_list_graph_items_fixed),
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
def tokens_view(request):
  ## order_by reverse - latest incident on top
  all_tokens = models.Tokens.objects.all().order_by('token_name')
  context = {'all_tokens':all_tokens}
  return render(request,'app/tokens.html',context=context) 

# Token create view
class TokenCreateView(LoginRequiredMixin,CreateView):
    model = Tokens
    form_class = TokenForm
    success_url = reverse_lazy('app:tokens_view')

class TokenDeleteView(LoginRequiredMixin, DeleteView):
    model = Tokens
    success_url = reverse_lazy('app:tokens_view')

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

## Update: not using this
def load_credentials(request):
    #credential_id = request.GET.get('credential')
    all_credentials = models.Credentials.objects.all().order_by('pk')
    context = {'all_credentials':all_credentials}
    return render(request, 'app/credentials_dropdown_list_options.html', context=context)

## credential list view --> template/app/credentials.html
def credentials_view(request):
    ## order_by managed nodes
    all_credentials = models.Credentials.objects.all().order_by('id')
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
@authentication_classes([])
@permission_classes([])
def incident_report(request):
    #authentication_classes = [] #disables authentication
    #permission_classes = [] #disables permission
    #permission_classes = (IsAuthenticated) 

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

        ## fetch the token and verify
        access_token = request.query_params.get("token")
        check_token = models.Tokens.objects.all().filter(token_value=access_token)


        incident_serializer = IncidentsSerializerNew(data=incident_data, context={
           "incident_hostname": request.query_params.get("source_hostname"),
        })

        my_incident_hostname = request.query_params.get("source_hostname")
        this_incident_report_agent = request.META['HTTP_USER_AGENT']
        #new_log = open( 'application_logs/logs', "a")
        #new_log.write('\n' + my_incident_hostname + json.dumps( incident_data ))
        #new_log.close()
        if '.ansible/tmp/ansible-tmp' in incident_data['output']:
            #pass
            if incident_serializer.is_valid():
                #incident_serializer.save    (incident_hostname=my_incident_hostname)
                return JsonResponse(incident_serializer.data,   status=status.HTTP_204_NO_CONTENT) 
            return JsonResponse(incident_serializer.errors,     status=status.HTTP_400_BAD_REQUEST)
            #return incident_data
        elif 'FALCO_OGRULE' in incident_data['rule']:
            if incident_serializer.is_valid():
                incident_serializer.save(incident_hostname=my_incident_hostname, incident_report_agent=this_incident_report_agent)
                #print(incident_serializer.data)
                return JsonResponse(incident_serializer.data, status=status.HTTP_201_CREATED) 
            return JsonResponse(incident_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #return incident_data
        else:
            #pass
            if incident_serializer.is_valid():
                #incident_serializer.save    (incident_hostname=my_incident_hostname)
                return JsonResponse(incident_serializer.data,   status=status.HTTP_204_NO_CONTENT) 
            return JsonResponse(incident_serializer.errors,     status=status.HTTP_400_BAD_REQUEST)            


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def incident_fix(request):

    #permission_classes = (IsAuthenticated)

    if request.method == 'GET':
        #all_incidents = models.Incidents.objects.all().filter(incident_status='PENDING').order_by('incident_time').first()
        all_incidents = models.Incidents.objects.all().filter(incident_status='PENDING').order_by('incident_time')[0:1]
        #print(len(all_incidents))
        if len(all_incidents) > 0:
            try:
                for incident in all_incidents.iterator():
                    #print(incident.incident_rule)

                    this_incident_id = incident.id
                    #print(this_incident_id)
                    this_hostname = incident.incident_hostname
                    rule_detected = incident.incident_rule
                    #return Response(rule_detected)
                    managed_node = models.ManagedNodes.objects.all().filter(instance_name=this_hostname).order_by       ('instance_name').first()
                    if managed_node != None:
                        node_name = getattr(managed_node,'instance_name')
                        node_connection_name = getattr(managed_node,'instance_name_connection')
                        node_connection_method = getattr(managed_node,'instance_credential')

                        try:
                            rule_list = models.Rules.objects.all().filter(rule_name = rule_detected).order_by       ('rule_name').first()
                            #print(len(rule_list))
                            if type(rule_list) != type(None):
                                #print("No rules !!!")
                                #pass
                                #if len(rule_list) > 0:
                                rule_fix_playbook = getattr(rule_list,'rule_fix_playbook')
                                job_data = { "incident_id": this_incident_id,
                                                "managed_node": node_name, 
                                                "node_connection_name": node_connection_name,
                                                "node_connection_method": node_connection_method,
                                                "rule_fix_playbook": rule_fix_playbook,
                                                "pending_incidents": "YES"
                                              }
                                return Response(job_data)
                                #else:
                                #    print("No Rules")
                            elif type(rule_list) == type(None):
                                ####### if no matching rules, then update incident  #####
                                incident.incident_status = "NO RULES FOUND"
                                incident.incident_fix_comments = "Unable to find any matching rule to remediate"
                                incident.save()

                                job_data = { "incident_id": this_incident_id,
                                          "managed_node":"NA",
                                          "node_connection_name": "NA",
                                          "node_connection_method": "NA",
                                          "rule_fix_playbook": "NA",
                                          "pending_incidents": "NO"
                                                  }
                                return Response(job_data)

                        except Exception as ansible_exception:
                            #print(ansible_exception)
                            print("No rules found: " + str(ansible_exception)  )
                            job_data = { "incident_id": "NA",
                                          "managed_node":"NA",
                                          "node_connection_name": "NA",
                                          "node_connection_method": "NA",
                                          "rule_fix_playbook": "NA",
                                          "pending_incidents": "NO"
                                        }
                            return Response(job_data)
            except Exception as incident_exception:
                job_data = { "incident_id": "NA",
                          "managed_node":"NA",
                          "node_connection_name": "NA",
                          "node_connection_method": "NA",
                          "rule_fix_playbook": "NA",
                          "pending_incidents": "NO"
                        }
                return Response(job_data)              
        else:
            job_data = { "incident_id": "NA",
                          "managed_node":"NA",
                          "node_connection_name": "NA",
                          "node_connection_method": "NA",
                          "rule_fix_playbook": "NA",
                          "pending_incidents": "NO"
                        }
            return Response(job_data)
            
    elif request.method == 'POST':
        message = {"incident_status": "Updating"}
        try:
            incident_fix_data = JSONParser().parse(request)
            print(incident_fix_data['incident_id'])
            this_incident_id = incident_fix_data['incident_id']
            this_incident = models.Incidents.objects.all().filter(id=this_incident_id)
            for incident in this_incident.iterator():
                try:
                    incident.incident_status = incident_fix_data['incident_status']
                    incident.incident_time_fixed = incident_fix_data['incident_time_fixed']
                    incident.incident_fix_comments = incident_fix_data['incident_fix_comments']
                    incident.save()
                    message = {"incident_status": "Updated"}
                    return JsonResponse(message, status=status.HTTP_202_ACCEPTED)
                except Exception as incident_save_exception:
                    print("Error: " + str(incident_save_exception))
                    return Response("Unable to save record; something went wrong !")
            
        except Exception as job_fix_exception:
            print("Error: " + str(job_fix_exception))
            return Response("Something went wrong !")


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)