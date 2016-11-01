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
                    return HttpResponseRedirect('/omp/dash_student/')
            elif usertype == "Supervisor":
                supervisor = Supervisor.objects.get(pk=username)
                if supervisor is not None:
                    permission = ''
                    return HttpResponseRedirect('/omp/dash_supervisor/')
            elif usertype == "Administrator":
                admin = Administrator.objects.get(pk=username)
                if admin is not None:
                    permission = 'Admin'
                    return HttpResponseRedirect('/omp/dash_admin/')
        else:
            # Return user to the homepage (replace later).
            return render_to_response('omp/home.html')

    return render(request, 'omp/login.html')


def user_logout(request):
    logout(request)
    return render_to_response('omp/logout.html')


@login_required(login_url="/omp/login/")
def studentdash(request):
    global permission
    if permission == "Student":
        return render_to_response('omp/dash_student.html', {'name': request.user.username})
    elif permission == "Supervisor":
        return HttpResponseRedirect('/omp/dash_supervisor/')
    else:
        return HttpResponseRedirect('/omp/dash_admin/')


@login_required(login_url="/omp/login/")
def supervisordash(request):
    global permission
    if permission == "Supervisor":
        return render_to_response('omp/dash_supervisor.html', {'name': request.user.username})
    elif permission == "Admin":
        return HttpResponseRedirect('/omp/dash_admin/')
    else:
        return HttpResponseRedirect('/omp/dash_student/')


@login_required(login_url="/omp/login/")
def admindash(request):
    global permission
    if permission == "Administrator":
        return render_to_response('omp/dash_admin.html', {'name': request.user.username})
    elif permission == "Supervisor":
        return HttpResponseRedirect('/omp/dash_supervisor/')
    else:
        return HttpResponseRedirect('/omp/dash_student/')


@login_required(login_url="/omp/login/")
def adminpanel(request):
    return HttpResponse("This is for admins only! Go <a href='/omp/'>back!</a>")


@login_required(login_url="/omp/login/")
def categories(request):

    # contsruct list of categories and order it by name
    category_list = Category.objects.order_by('name')
    context_dict = {'categories': category_list}

    # Render and send back response
    return render(request, 'omp/categories.html', context=context_dict)


@login_required(login_url="/omp/login/")
def projects(request):

    #construct list of projects and order it by name
    project_list = Project.objects.order_by('name')
    context_dict = {'projects': project_list}

    # Render and send back response
    return render(request, 'omp/projects.html', context=context_dict)


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
            #redirect to dashboard after adding category
            return dashboard(request)
        else:
        # The supplied form contained errors -
        # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'omp/add_category.html', {'form': form})