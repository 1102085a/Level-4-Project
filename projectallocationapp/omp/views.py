from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from omp.forms import CategoryForm, ProjectForm, StudentForm, SupervisorForm, AdminForm, PreferenceForm
from omp.models import User, Project, Category, Student, Supervisor, Administrator, PrefListEntry, SiteConfiguration


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
        if user:  # user exists
            login(request, user)
            if usertype == "Student":
                student = Student.objects.get(user=user)
                if student is not None:
                    request.session['permission'] = "Student"
            elif usertype == "Supervisor":
                supervisor = Supervisor.objects.get(user=user)
                if supervisor is not None:
                    request.session['permission'] = "Supervisor"
            elif usertype == "Administrator":
                admin = Administrator.objects.get(user=user)
                if admin is not None:
                    request.session['permission'] = "Administrator"

            urlresponse = '/omp/' + username + '/dashboard/'
            return HttpResponseRedirect(urlresponse)

        else:
            # Display error message.
            # Bad login details were provided. So we can't log the user in.
            user = User.objects.filter(username=username)
            if user:  # username exists, so password must be incorrect
                error_message = "Incorrect password for username {0}".format(username)
            else:  # username doesn't exist
                error_message = "Username {0} not recognised".format(username)

    return render(request, 'omp/login.html', {'login_message': error_message})


def user_logout(request):
    logout(request)
    return render_to_response('omp/home.html')


@login_required(login_url="/omp/login/")
def dashboard(request, username):

    permission = request.session['permission']  # get user permission from session
    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    context_dict['error_message'] = ""
    context_dict['delete_message'] = ""
    user = request.user
    usertype = getuserobject(request)  # get user object for permission
    context_dict['user'] = user

    if request.method == 'POST':
        if 'Next' in request.POST:
            sc.site_stage += 1
            sc.save()
            context_dict['stage'] = sc.site_stage
            return render(request, 'omp/dash_admin.html', context=context_dict)
        elif 'Previous' in request.POST:
            sc.site_stage -= 1
            sc.save()
            context_dict['stage'] = sc.site_stage
            return render(request, 'omp/dash_admin.html', context=context_dict)
        if 'Delete' in request.POST:
            pref = request.POST.get('Delete', None)
            prefnum = pref[-1:]
            PrefListEntry.objects.get(student=usertype, rank=prefnum).delete()
            context_dict['delete_message'] = "Preference " + prefnum + " deleted"
            return render(request, 'omp/dash_student.html', context=context_dict)



    # check user permission
    if permission == "Student":
        context_dict['student'] = usertype
        try:
            student_preferences = PrefListEntry.objects.filter(student__user=user).order_by('rank')
            context_dict['preferences'] = student_preferences
        except PrefListEntry.DoesNotExist:
            context_dict['preferences'] = None
        return render(request, 'omp/dash_student.html', context=context_dict)
    if permission == "Supervisor":
        category_list = usertype.category.all()
        super_projects = Project.objects.filter(supervisor=usertype)
        context_dict['supervisor'] = usertype
        context_dict['categories'] = category_list
        context_dict['projects'] = super_projects
        return render(request, 'omp/dash_supervisor.html', context=context_dict)
    if permission == "Administrator":
        context_dict['admin'] = usertype
        return render(request, 'omp/dash_admin.html', context=context_dict)
    else:
        return HttpResponseRedirect('/omp/login')


# checks user permission and retrieves appropriate object
def getuserobject(request):
    permission = request.session['permission']
    if permission == "Student":
        return Student.objects.get(user=request.user)
    if permission == "Supervisor":
        return Supervisor.objects.get(user=request.user)
    if permission == "Administrator":
        return Administrator.objects.get(user=request.user)


@login_required(login_url="/omp/login/")
def category(request, category_name_slug):
    context_dict = {}

    try:
        user = request.user
        context_dict['user'] = user

        permission = request.session['permission'].lower()
        usertype = getuserobject(request)
        context_dict[permission] = usertype

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
    error = ""

    if request.method == 'POST':  # Get values from form fields
        user = request.user
        s = Student.objects.get(user=user)
        p = Project.objects.get(slug=project_name_slug)
        # check which form was submitted
        if 'Favourite' in request.POST:
            s.favourites.add(p)
            s.save()
            confirmation = "Project added to favourites."
            context_dict['fave_confirm_message'] = confirmation
        elif 'Preferences' in request.POST:
            success = True
            pref = request.POST.get('ranking', None)
            if not p.softEng and s.softEng:
                error = "You must select software engineering projects."
                success = False
            else:
                prefList = PrefListEntry.objects.filter(student__user=user).order_by('rank')
                if len(prefList) == 5:
                    error = "You already have five projects preferred. Please delete one from the dashboard."
                    success = False
                else:
                    for proj in prefList:
                        if p.name == proj.project.name:
                            error = "You already have this project in your preferences."
                            success = False
                        print(pref + " " + str(proj.rank))
                        if int(pref) == int(proj.rank):
                            error = "Project already at this rank, please select a different ranking."
                            success = False
                    else:
                        if not checkSupervisors(prefList, proj):
                            error = "You already have too many projects under this supervisor."
                            success = False
            print(success)
            if success:
                p = PrefListEntry(project=p, student=s, rank=pref)
                p.save()
                confirmation = "Project saved to preferences at " + pref + "."

            context_dict['error_message'] = error
            context_dict['pref_confirm_message'] = confirmation

    try:

        user = request.user
        if 'username' not in request.session:
            request.session['username'] = user.username
        username = request.session['username']
        student = getuserobject(request)
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


def checkSupervisors(prefList, proj):
    supervisor = proj.project.supervisor
    count = 0
    for pref in prefList:
        if pref.project.supervisor == supervisor:
            count += 1
    if count > 2:
        return False
    return True


@login_required(login_url="/omp/login/")
def add_category(request):
    context_dict = {}
    form = CategoryForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # get user info
    user = request.user
    context_dict['user'] = user

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Redirect to dashboard after adding category
            return dashboard(request)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'omp/add_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def add_project(request):
    context_dict = {}
    form = ProjectForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # get user info
    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype
    if permission == "supervisor":
        category_list = usertype.category.all()
        context_dict['categories'] = category_list

    # HTTP POST?
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save to database
            form.save(commit=True)
            # Redirect to dashboard
            return dashboard(request)

    return render(request, 'omp/add_project.html', context=context_dict)


@login_required(login_url="/omp/login/")
def add_student(request):
    context_dict = {}
    form = StudentForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # get user info
    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype

    # HTTP POST?
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save to database
            form.save(commit=True)
            # Redirect to dashboard
            return dashboard(request, user.username)

    return render(request, 'omp/add_student.html', context=context_dict)


@login_required(login_url="/omp/login/")
def supervisor_list(request, username):

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    supervisors = Supervisor.objects.all().order_by('user__username')
    context_dict["supervisors"] = supervisors
    return render(request, 'omp/admin_supervisor.html', context=context_dict)


@login_required(login_url="/omp/login/")
def student_list(request, username):

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    students = Student.objects.all().order_by('user__username')
    context_dict["students"] = students
    return render(request, 'omp/admin_student.html', context=context_dict)


@login_required(login_url="/omp/login/")
def project_list(request, username):

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    projects = Project.objects.all().order_by('name')
    context_dict["projects"] = projects
    return render(request, 'omp/admin_project.html', context=context_dict)


@login_required(login_url="/omp/login/")
def category_list(request, username):

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    categories = Category.objects.all().order_by('name')
    context_dict["categories"] = categories
    return render(request, 'omp/admin_category.html', context=context_dict)


@login_required(login_url="/omp/login/")
def preference_list(request, username):

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    prefs = PrefListEntry.objects.all().order_by('student__username__username')
    context_dict["prefs"] = prefs
    return render(request, 'omp/admin_prefs.html', context=context_dict)


@login_required(login_url="/omp/login/")
def edit_category(request, category_name_slug):
    context_dict = {}
    context_dict['confirm_message'] = ""

    try:
        user = request.user
        context_dict['user'] = user

        permission = request.session['permission'].lower()
        usertype = getuserobject(request)
        context_dict[permission] = usertype

        category = Category.objects.get(slug=category_name_slug)

        form = CategoryForm(initial={'name': category.name})

        context_dict['form'] = form
        context_dict['form_errors'] = form.errors

    except Category.DoesNotExist:
        context_dict['projects'] = None
        context_dict['category'] = None

        # A HTTP POST?
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save(commit=True)
                context_dict['confirm_message'] = "Category Saved."
            return render(request, 'omp/edit_category.html', context=context_dict)

    return render(request, 'omp/edit_category.html', context=context_dict)




