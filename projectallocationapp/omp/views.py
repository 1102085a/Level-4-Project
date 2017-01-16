from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from omp.forms import CategoryForm, ProjectForm
from omp.models import User, Project, Category, Student, Supervisor, Administrator, PrefListEntry


#permission = ''


def home(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key 'message' is the same as {{ message }} in the template!
    context_dict = {'construction': "This page is under construction!"}

    # Render and send back response
    return render(request, 'omp/home.html', context=context_dict)


def user_login(request):
    error_message = ""

    if request.method == 'POST':  # Get values from form fields
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        usertype = request.POST.get('permission', None)
        user = authenticate(username=username, password=password)
        request.session['username'] = username  # store username for session
        if user: # user exists
            login(request, user)
            if usertype == "Student":
                student = Student.objects.get(pk=username)
                if student is not None:
                    request.session['permission'] = "Student"
            elif usertype == "Supervisor":
                supervisor = Supervisor.objects.get(pk=username)
                if supervisor is not None:
                    request.session['permission'] = "Supervisor"
            elif usertype == "Administrator":
                admin = Administrator.objects.get(pk=username)
                if admin is not None:
                    request.session['permission'] = "Administrator"

            urlresponse = '/omp/dashboard/' + username
            return HttpResponseRedirect(urlresponse)

        else:
            # Display error message.
            # Bad login details were provided. So we can't log the user in.
            user = User.objects.filter(username=username)
            if user:  # username exists, so password must be incorrect
                error_message = "Incorrect password for username {0}".format(username)
            else:  # username doesn't exist
                error_message = "Username {0} not recognised".format(username)

    return render(request, 'omp/login.html', {'login_message' : error_message})


def user_logout(request):
    logout(request)
    return render_to_response('omp/logout.html')


@login_required(login_url="/omp/login/")
def dashboard(request, username):
    permission = request.session['permission']  # get user permission from session
    context_dict = {}
    context_dict['error_message'] = ""
    user = request.user
    usertype = getuserobject(username, request)  # get user object for permission
    context_dict['user'] = user

    # check user permission
    if permission == "Student":
        context_dict['student'] = usertype
        try:
            student_preferences = PrefListEntry.objects.filter(student__id=username).order_by('rank')
            context_dict['preferences'] = student_preferences
            print(context_dict['preferences'])
        except PrefListEntry.DoesNotExist:
            context_dict['preferences'] = None
        return render_to_response('omp/dash_student.html', context=context_dict)
    if permission == "Supervisor":
        category_list = usertype.category.all()
        context_dict['supervisor'] = usertype
        context_dict['categories'] = category_list
        return render_to_response('omp/dash_supervisor.html', context=context_dict)
    if permission == "Administrator":
        context_dict['admin'] = usertype
        return render_to_response('omp/dash_admin.html', context=context_dict)
    else:
        return HttpResponseRedirect('/omp/login')


# checks user permission and retrieves appropriate object
def getuserobject(username, request):
    permission = request.session['permission']
    if permission == "Student":
        return Student.objects.get(pk=username)
    if permission == "Supervisor":
        return Supervisor.objects.get(pk=username)
    if permission == "Administrator":
        return Administrator.objects.get(pk=username)


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
    confirmation = ""
    error=""

    if request.method == 'POST':  # Get values from form fields
        username = request.session['username']
        s = Student.objects.get(pk=username)
        p = Project.objects.get(slug=project_name_slug)
        # check which form was submitted
        if 'Favourite' in request.POST:
            s.favourites.add(p)
            s.save()
            confirmation = "Project added to favourites."
            context_dict['fave_confirm_message'] = confirmation
        elif 'Preferences' in request.POST:
            pref = request.POST.get('ranking', None)
            p = PrefListEntry(project=p, student=s, rank=pref)
            p.save()
            confirmation = "Project saved to preferences."
            context_dict['pref_confirm_message'] = confirmation

    try:

        user = request.user
        if 'username' not in request.session:
            request.session['username'] = user.username
        username = request.session['username']
        student = getuserobject(username, request)
        context_dict['user'] = user
        context_dict['student'] = student
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
            return dashboard(request)
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
            return HttpResponseRedirect('omp/dashboard')
        else:
            print(form.errors)
    return render(request, 'omp/add_project.html', {'form': form})

