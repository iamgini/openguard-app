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
                  'incident_output')

## incident serializer for falco
#class IncidentsSerializerNew(serializers.HyperlinkedModelSerializer):
class IncidentsSerializerNew(serializers.ModelSerializer):
    time = serializers.DateTimeField(source='incident_time')
    priority = serializers.CharField(source='incident_priority')
    rule = serializers.CharField(source='incident_rule')
    output = serializers.CharField(source='incident_output')
    #hostname = serializers.CharField(source='incident_hostname')
    #hostname = serializers.SerializerMethodField('incident_hostname')
    #output_fields = serializers.CharField(source='incident_output_fields_new')
    #def get_hostname(self):
    #    hostname = self.kwargs['hostname']
    #    return hostname

    incident_hostname = serializers.SerializerMethodField()
    
    @classmethod
    def get_incident_hostname(self, object):
        """getter method to add field incident_hostname"""
        return 'hostname'

    class Meta:
        model = Incidents
        fields = ('id',
                  'incident_hostname',
                  'incident_time_reported',
                  'time', 
                  'priority',
                  'rule',
                  'output',)

    #def to_representation(self, instance):
    #  representation = super().to_representation(instance)
    #  if instance.name!='': #condition
    #     representation['email']=instance.name+"@xyz.com"#adding key and value
    #     representation['currency']=instance.task.profile.currency #adding key and value some other relation field
    #     return representation
    #  return representation