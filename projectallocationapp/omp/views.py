from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from omp.forms import CategoryForm, ProjectForm
from omp.models import User, Project, Category


def home(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key 'message' is the same as {{ message }} in the template!
    context_dict = {'construction': "This page is under construction!"}

    # Render and send back response
    return render(request, 'omp/home.html', context=context_dict)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/omp/dash/')
        else:
            # Return an 'invalid login' error message.
            return render_to_response('omp/home.html')

    return render(request, 'omp/login.html')


def logout(request):
    logout(request)
    return render_to_response('omp/logout.html')


#@login_required("/omp/login")
def dashboard(request):
    return render_to_response('omp/dash.html', {'name': request.user.username})


def adminpanel(request):
    return HttpResponse("This is for admins only! Go <a href='/omp/'>back!</a>")


def categories(request):

    # contsruct list of categories and order it by name
    category_list = Category.objects.order_by('name')
    context_dict = {'categories': category_list}

    # Render and send back response
    return render(request, 'omp/categories.html', context=context_dict)


def projects(request):

    #construct list of projects and order it by name
    project_list = Project.objects.order_by('name')
    context_dict = {'projects': project_list}

    # Render and send back response
    return render(request, 'omp/projects.html', context=context_dict)


def projectpage(request):
    return HttpResponse("This is where the project will be! Go <a href='/omp/dash/'>back!</a>")


def add_category(request):
    form = CategoryForm

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            #redirect to dashboard after adding category
            return dashboard(request)
        else:
        # The supplied form contained errors -
        # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'omp/add_category.html', {'form': form})