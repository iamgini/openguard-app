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
                  'incident_hostname',
                  'incident_time_reported',
                  'incident_time', 
                  'incident_priority',
                  'incident_rule',
                  'incident_output',
                  'incident_report_agent')

## incident serializer for falco
#class IncidentsSerializerNew(serializers.HyperlinkedModelSerializer):
class IncidentsSerializerNew(serializers.ModelSerializer):
    time = serializers.DateTimeField(source='incident_time')
    priority = serializers.CharField(source='incident_priority')
    rule = serializers.CharField(source='incident_rule')
    output = serializers.CharField(source='incident_output')

    ## fetch arguments from url
    ## https://stackoverflow.com/questions/66745219/django-rest-framework-use-url-parameter-in-serializer
    incident_hostname = serializers.SerializerMethodField()
    def get_incident_hostname(self, obj):
        return self.context.get('incident_hostname')

    class Meta:
        model = Incidents
        fields = ('id',
                  'incident_hostname',
                  'incident_time_reported',
                  'time', 
                  'priority',
                  'rule',
                  'output',)