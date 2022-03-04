from django.urls import path, include
#from django.conf.urls import url 
## Rest API
from rest_framework import routers
from . import views

router_nodes = routers.DefaultRouter()
router_nodes.register(r'managednodes', views.ManagedNodesViewSet)

router_incidents = routers.DefaultRouter()
router_incidents.register(r'incidents', views.IncidentsViewSet)

app_name = 'app'
urlpatterns = [
  #path('', views.index,name='index'),
  path('',views.home_view,name='home_view'),
  #path('home/',views.home_view,name='home_view')
  #path('test/',views.index,name='app')  # /app --> demo_site urls.py
  ## for login
  #path('login/',views.home_view,name='home_view')
  
  ## API URLS
  path('api/nodes/', include(router_nodes.urls)),
  path('api/nodesv2/', views.nodes_list, name='nodes_list_api'),
  path('api/incidents/', include(router_incidents.urls)),
  path('api/incident_report/', views.incident_report,name='incident_report_api'),
  #path('api/incident_report/<str:hostname>/', views.incident_report,name='incident_report_api'),
  #<str:topic>/

  #url(r'^api/tutorials$', views.tutorial_list),
]
