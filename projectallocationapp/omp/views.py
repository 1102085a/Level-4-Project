from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from omp.forms import CategoryForm, ProjectForm
from omp.models import User, Project, Category, Student, Supervisor, Administrator


permission = ''


def home(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key 'message' is the same as {{ message }} in the template!
    context_dict = {'construction': "This page is under construction!"}

    # Render and send back response
    return render(request, 'omp/home.html', context=context_dict)


def user_login(request):

    global permission
    if request.method == 'POST':  # Get values from form fields
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        usertype = request.POST.get('permission', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if usertype == "Student":
                student = Student.objects.get(pk=username)
                if student is not None:
                    permission = 'Student'
            elif usertype == "Supervisor":
                supervisor = Supervisor.objects.get(pk=username)
                if supervisor is not None:
                    permission = 'Supervisor'
            elif usertype == "Administrator":
                admin = Administrator.objects.get(pk=username)
                if admin is not None:
                    permission = 'Admin'

        else:
            # Return user to the homepage (replace later).
            return render_to_response('omp/home.html')

        urlresponse = '/omp/dashboard/' + username

        return HttpResponseRedirect(urlresponse)

    return render(request, 'omp/login.html')


def user_logout(request):
    logout(request)
    return render_to_response('omp/logout.html')


@login_required(login_url="/omp/login/")
def dashboard(request, username):
    global permission
    context_dict = {}
    category_list = Category.objects.order_by('id')
    user = request.user
    context_dict['categories'] = category_list
    context_dict['user'] = user

    if permission == "Student":
        return render_to_response('omp/dash_student.html', context=context_dict)
    if permission == "Supervisor":
        supervisor = Supervisor.objects.get(pk=username)
        context_dict['supervisor'] = supervisor
        return render_to_response('omp/dash_supervisor.html', context=context_dict)
    if permission == "Administrator":
        return render_to_response('omp/dash_admin.html', context=context_dict)
    else:
        return HttpResponseRedirect('/omp/login')


@login_required(login_url="/omp/login/")
def adminpanel(request):
    return HttpResponse("This is for admins only! Go <a href='/omp/'>back!</a>")


@login_required(login_url="/omp/login/")
def category(request, category_name_slug):
    context_dict = {}

    try:
        user = request.user
        context_dict['user'] = user

        category = Category.objects.get(slug=category_name_slug)
        projects = Project.objects.filter(category=category)

        context_dict['projects'] = projects
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['projects'] = None
        context_dict['category'] = None

    return render(request, 'omp/category.html', context=context_dict)


@login_required(login_url="/omp/login/")
def project(request, category_name_slug, project_name_slug):

    context_dict = {}

    try:
        # Can we find a name slug with the given name?
        # If we can't, .get() raises a DoesNotExist exception.
        category = Category.objects.get(slug=category_name_slug)
        project = Project.objects.get(slug=project_name_slug)
        context_dict['category'] = category
        context_dict['project'] = project

    except Project.DoesNotExist:
        context_dict['category'] = None
        context_dict['project'] = None

    # Render and send back response
    return render(request, 'omp/project.html', context=context_dict)


@login_required(login_url="/omp/login/")
def projectpage(request):
    return HttpResponse("This is where the project will be! Go <a href='/omp/dash/'>back!</a>")


@login_required(login_url="/omp/login/")
def add_category(request):
    form = CategoryForm

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # redirect to dashboard after adding category
            return admindash(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'omp/add_category.html', {'form': form})


@login_required(login_url="/omp/login/")
def add_project(request):
    form = ProjectForm

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('omp/dash_supervisor')
        else:
            print(form.errors)
    return render(request, 'omp/add_project.html', {'form': form})