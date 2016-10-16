from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key 'message' is the same as {{ message }} in the template!
    context_dict = {'construction': "This page is under construction!"}

    # Render and send back response
    return render(request, 'omp/home.html', context=context_dict)

def dashboard(request):
    return render(request, 'omp/dash.html')

def adminpanel(request):
    return HttpResponse("This is for admins only! Go <a href='/omp/'>back!</a>")

def categories(request):
    return HttpResponse("This is where the categories will be! Go <a href='/omp/dash/'>back!</a>")

def projects(request):

    #contruct list of categories and order it by name
    project_list = Project.objects.order_by('name')
    context_dict = {'projects': project_list}

    # Render and send back response
    return render(request, 'omp/projects.html', context=context_dict)

def projectpage(request):
    return HttpResponse("This is where the project will be! Go <a href='/omp/dash/'>back!</a>")
