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
                  'incident_time', 
                  'incident_priority',
                  'incident_rule',
                  'incident_output',
                  'incident_output_fields')