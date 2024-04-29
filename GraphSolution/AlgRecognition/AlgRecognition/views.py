from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# def index(request):
#   template = loader.get_template('index.html')
#   return HttpResponse(template.render())

def index(request):
    return render(request, 'index.html')
    #return HttpResponse("Hello, world. You're at the polls index.")


