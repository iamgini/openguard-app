## redirect for url redirection after user submit data
from django.shortcuts import render,redirect
from django.urls import reverse
#from .import models
from django.http import HttpResponse
from django.http.response import Http404, HttpResponse, HttpResponseNotFound

# Create your views here.
def index(request):
  return HttpResponse("This is app")

def home_view(request):
  #home template file
  return render(request,'app/home.html')  

