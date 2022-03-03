# app/serializers.py
from rest_framework import serializers

from .models import ManagedNodes, Incidents

class ManagedNodesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ManagedNodes
        fields = ('id', 
                  'instance_name', 
                  'instance_name_connection',
                  'instance_credential',
                  'date_time')

## incident serializer
class IncidentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Incidents
        fields = ('id', 
                  'incident_time_reported',
                  'incident_time', 
                  'incident_priority',
                  'incident_rule',
                  'incident_output')

## incident serializer for falco
#class IncidentsSerializerNew(serializers.HyperlinkedModelSerializer):
class IncidentsSerializerNew(serializers.ModelSerializer):
    time = serializers.DateTimeField(source='incident_time')
    priority = serializers.CharField(source='incident_priority')
    rule = serializers.CharField(source='incident_rule')
    output = serializers.CharField(source='incident_output')
    #output_fields = serializers.CharField(source='incident_output_fields_new')

    class Meta:
        model = Incidents
        fields = ('id', 
                  'incident_time_reported',
                  'time', 
                  'priority',
                  'rule',
                  'output',)
