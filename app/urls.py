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
                    CredentialDeleteView)

router_nodes = routers.DefaultRouter()
router_nodes.register(r'managednodes', views.ManagedNodesViewSet)

router_incidents = routers.DefaultRouter()
router_incidents.register(r'incidents', views.IncidentsViewSet)

app_name = 'app'
urlpatterns = [
  #path('', views.index,name='index'),
  path('',views.home_view,name='home_view'),
  ## app dashboard
  path('dashboard/',views.dashboard_view,name='dashboard_view'),

  ## incident list
  path('incidents/',views.incident_view,name='incident_view'),

  ## managed nodes list
  path('managed_nodes/',views.managed_nodes_view,name='managed_nodes_view'),
  path('create_node',ManagedNodeCreateView.as_view(),name='create_node'),
  path('update_node/<int:pk>/',ManagedNodeUpdateView.as_view(),name='update_node'),
  path('delete_node/<int:pk>/',ManagedNodeDeleteView.as_view(),name="delete_node"),

  ## credentials list
  path('credentials/',views.credentials_view,name='credentials_view'),
  path('create_credential/',CredentialCreateView.as_view(),name='create_credential'),
  path('update_credential/<int:pk>/',CredentialUpdateView.as_view(),name='update_credential'),
  path('delete_credential/<int:pk>/',CredentialDeleteView.as_view(),name="delete_credential"),

  

  #path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard_view'),
  #path('home/',views.home_view,name='home_view')
  
  ## API URLS
  path('api/nodes/', include(router_nodes.urls)),
  path('api/nodesv2/', views.nodes_list, name='nodes_list_api'),
  path('api/incidents/', include(router_incidents.urls)),
  path('api/incident_report/', views.incident_report,name='incident_report_api'),
  #path('api/incident_report/<str:hostname>/', views.incident_report,name='incident_report_api'),
  #<str:topic>/

  #url(r'^api/tutorials$', views.tutorial_list),
]
