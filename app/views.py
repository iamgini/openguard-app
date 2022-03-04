## redirect for url redirection after user submit data
from django.shortcuts import render,redirect
from django.urls import reverse
#from .import models
from django.http import HttpResponse
from django.http.response import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from rest_framework.parsers import JSONParser 

## REST API
from rest_framework import viewsets, status
from .serializers import ManagedNodesSerializer, IncidentsSerializer, IncidentsSerializerNew
from .models import ManagedNodes, Incidents

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
def incident_report(request,hostname):
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
        incident_hostname = {"hostname":"hostname"}
        incident_data = JSONParser().parse(request)
        
        new_log = open( 'application_logs/logs', "a")
        new_log.write('\n' + hostname + json.dumps( incident_data ))
        new_log.close()


        #incident_hostname = JSONParser().parse(request.POST)
        incident_serializer = IncidentsSerializerNew(data=incident_data)

        if incident_serializer.is_valid():
            incident_serializer.save()
            return JsonResponse(incident_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(incident_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return incident_data
        