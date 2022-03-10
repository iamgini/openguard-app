from django.urls import path, include
#from django.conf.urls import url 
## Rest API
from rest_framework import routers
from . import views
from django.views.generic.base import TemplateView

from .views import (ManagedNodeCreateView,
                    ManagedNodeUpdateView,
                    ManagedNodeDeleteView,
                    CredentialCreateView,
                    CredentialUpdateView,
                    CredentialDeleteView,
                    RuleCreateView,
                    RuleUpdateView,
                    RuleDeleteView
                    )

router_nodes = routers.DefaultRouter()
router_nodes.register(r'managednodes', views.ManagedNodesViewSet)

router_incidents = routers.DefaultRouter()
router_incidents.register(r'incidents', views.IncidentsViewSet)

app_name = 'app'
urlpatterns = [
  #path('', views.index,name='index'),
  #path('',views.home_view,name='home_view'),
  path('',views.dashboard_view,name='dashboard_view'),
  ## app dashboard
  path('dashboard/',views.dashboard_view,name='dashboard_view'),

  ## incident list
  path('incidents/',views.incident_view,name='incident_view'),
  path('incidents/demo',views.incident_demo,name='incident_demo'),

  ## for running jobs
  path('jobs/run',views.run_fix_jobs,name='run_fix_jobs'),

  ## managed nodes list
  path('managed_nodes/',views.managed_nodes_view,name='managed_nodes_view'),
  path('managed_nodes/create',ManagedNodeCreateView.as_view(),name='create_node'),
  path('managed_nodes/update/<int:pk>/',ManagedNodeUpdateView.as_view(),name='update_node'),
  path('managed_nodes/delete/<int:pk>/',ManagedNodeDeleteView.as_view(),name="delete_node"),
  # for ajax loading of credentials
  path('load-credentials/', views.load_credentials, name='ajax_load_credentials'),

  ## credentials URLs
  path('credentials/',views.credentials_view,name='credentials_view'),
  path('credentials/create/',CredentialCreateView.as_view(),name='create_credential'),
  path('credentials/update/<int:pk>/',CredentialUpdateView.as_view(),name='update_credential'),
  path('credentials/delete/<int:pk>/',CredentialDeleteView.as_view(),name="delete_credential"),
  
  ## Rules URLs
  path('rules/',views.rules_view,name='rules_view'),
  path('rules/create/',RuleCreateView.as_view(),name='create_rule'),
  path('rules/update/<int:pk>/',RuleUpdateView.as_view(),name='update_rule'),
  path('rules/delete/<int:pk>/',RuleDeleteView.as_view(),name="delete_rule"),
  
  #path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard_view'),
  #path('home/',views.home_view,name='home_view')
  
  ## API URLS -
  path('api/nodes/', include(router_nodes.urls)),
  path('api/nodesv2/', views.nodes_list, name='nodes_list_api'),

  ## http://IP:8000/api/incidents/
  path('api/incidents/', include(router_incidents.urls)),
  path('api/incident_report/', views.incident_report,name='incident_report_api'),
  #path('api/incident_report/<str:hostname>/', views.incident_report,name='incident_report_api'),
  #<str:topic>/

  #url(r'^api/tutorials$', views.tutorial_list),
]
