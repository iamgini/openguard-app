from django.urls import path
from . import views

urlpatterns = [
  #path('', views.index,name='index'),
  path('',views.home_view,name='home_view')
  #path('home/',views.home_view,name='home_view')
  #path('test/',views.index,name='app')  # /app --> demo_site urls.py


  ## for login
  #path('login/',views.home_view,name='home_view')
  #
]
