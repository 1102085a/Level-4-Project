from django.shortcuts import render
from django.http import HttpResponse
from omp.models import User, Project, Category

def home(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key 'message' is the same as {{ message }} in the template!
    context_dict = {'construction': "This page is under construction!"}

    # Render and send back response
    return render(request, 'omp/home.html', context=context_dict)

def login(request):
    return render(request, 'omp/login.html')

def dashboard(request):
    return render(request, 'omp/dash.html')

def adminpanel(request):
    return HttpResponse("This is for admins only! Go <a href='/omp/'>back!</a>")

def categories(request):

    # contsruct list of categories and order it by name
    category_list = Category.objects.order_by('name')
    context_dict = {'categories': category_list}

    # Render and send back response
    return render(request, 'omp/categories.html', context=context_dict)

def projects(request):

    #construct list of categories and order it by name
    project_list = Project.objects.order_by('name')
    context_dict = {'projects': project_list}

    # Render and send back response
    return render(request, 'omp/projects.html', context=context_dict)

def projectpage(request):
    return HttpResponse("This is where the project will be! Go <a href='/omp/dash/'>back!</a>")

def show_user(request, user_id_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        user = User.objects.get(slug=user_id_slug)
        context_dict['user'] = user

    except User.DoesNotExist:

        # We get here if we didn't find the specified user.
        # Don't do anything -
        # the template will display the "no user" message for us.
        context_dict['user'] = None


    # Go render the response and return it to the client.
    return render(request, 'omp/dash.html', context_dict)