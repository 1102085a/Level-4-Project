from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'construction': "This page is under construction!"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'omp/home.html', context=context_dict)

def dashboard(request):
    return HttpResponse("This is the omp dashboard! <a href='/omp/'>Go to the homepage!</a>")

def adminpanel(request):
    return HttpResponse("This is for admins only! Go <a href='/omp/'>back!</a>")

