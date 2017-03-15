from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponseForbidden
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from omp.forms import CategoryForm, ProjectForm, StudentForm, SupervisorForm, AdminForm, PreferenceForm
from omp.models import User, Project, Category, Student, Supervisor, Administrator, PrefListEntry, SiteConfiguration
from algorithm import greedyAssignment


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
        if 'Match' in request.POST:
            reset()
            processlist = greedyAssignment()
            context_dict['processed'] = processlist
            return render(request, 'omp/matchresults.html', context=context_dict)

    # check user permission
    if permission == "Student":
        # Grab all our student info, including their preference list if it exists
        context_dict['student'] = usertype
        try:
            student_preferences = PrefListEntry.objects.filter(student__user=user).order_by('rank')
            context_dict['preferences'] = student_preferences
        except PrefListEntry.DoesNotExist:
            context_dict['preferences'] = None
        return render(request, 'omp/dash_student.html', context=context_dict)
    if permission == "Supervisor":
        # Grab all the supervisor information we need, their object, students, projects etc
        category_list = usertype.category.all()
        super_projects = Project.objects.filter(supervisor=usertype)
        try:
            assignedStudents = Student.objects.filter(project__supervisor=usertype)
            context_dict["assigned"] = assignedStudents
        except Student.DoesNotExist:
            context_dict["assigned"] = None
        context_dict['supervisor'] = usertype
        context_dict['categories'] = category_list
        context_dict['projects'] = super_projects
        return render(request, 'omp/dash_supervisor.html', context=context_dict)
    if permission == "Administrator":
        # we only need the admin object here
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


def reset():
    projects = list(Project.objects.all())
    supervisors = list(Supervisor.objects.all())

    print("Resetting matched data...")

    for project in projects:
        project.assigned = False
        project.save()

    for supervisor in supervisors:
        supervisor.assigned = 0
        supervisor.save()

    print("DONE.")


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
        projects = Project.objects.filter(category=category).order_by('name')

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
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()
    context_dict = {}
    form = CategoryForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors
    context_dict['itemname'] = "Category"

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
            return HttpResponseForbidden()

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'omp/add_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def add_project(request):
    # kick users with insufficient permissions
    if request.session["permission"] == "Student":
        return HttpResponseForbidden()

    context_dict = {}

    # get user info
    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype
    if permission == "supervisor":
        form = ProjectForm(initial={'supervisor': usertype})
        category_list = usertype.category.all()
        context_dict['categories'] = category_list
    else:
        form = ProjectForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors
    context_dict['itemname'] = "Project"
    
    # HTTP POST?
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save to database
            form.save(commit=True)
            # Redirect to dashboard
            return dashboard(request, user.username)

    return render(request, 'omp/add_project.html', context=context_dict)


@login_required(login_url="/omp/login/")
def add_student(request):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    form = StudentForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors
    context_dict['itemname'] = "Student"

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

    return render(request, 'omp/add_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def add_supervisor(request):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    form = SupervisorForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors
    context_dict['itemname'] = "Supervisor"

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

    return render(request, 'omp/add_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def add_admin(request):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    form = AdminForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors
    context_dict['itemname'] = "Administrator"

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

    return render(request, 'omp/add_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def add_preference(request):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    form = PreferenceForm
    context_dict['form'] = form
    context_dict['form_errors'] = form.errors
    context_dict['itemname'] = "Preference List"

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

    return render(request, 'omp/add_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def supervisor_list(request, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    supervisors = Supervisor.objects.all().order_by('user__username')
    context_dict["supervisors"] = supervisors
    return render(request, 'omp/admin_supervisor.html', context=context_dict)


@login_required(login_url="/omp/login/")
def student_list(request, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    students = Student.objects.all().order_by('user__username')
    context_dict["students"] = students
    return render(request, 'omp/admin_student.html', context=context_dict)


@login_required(login_url="/omp/login/")
def admin_list(request, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    admins = Administrator.objects.all().order_by('user__username')
    context_dict["admins"] = admins
    return render(request, 'omp/admin_admins.html', context=context_dict)


@login_required(login_url="/omp/login/")
def project_list(request, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    projects = Project.objects.all().order_by('name')
    context_dict["projects"] = projects
    return render(request, 'omp/admin_project.html', context=context_dict)


@login_required(login_url="/omp/login/")
def category_list(request, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    context_dict['delete_message'] = ""
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    categories = Category.objects.all().order_by('name')
    context_dict["categories"] = categories

    if request.method == 'POST':
        if 'Delete' in request.POST:
            cat = request.POST.get('Delete', None)
            cid = cat[-2:]
            Category.objects.get(pk=cid).delete()
            context_dict['delete_message'] = "Category deleted"

    return render(request, 'omp/admin_category.html', context=context_dict)


@login_required(login_url="/omp/login/")
def preference_list(request, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    sc = SiteConfiguration.objects.get()
    context_dict['stage'] = sc.site_stage
    prefs = PrefListEntry.objects.all().order_by('student__user__username')
    context_dict["prefs"] = prefs
    return render(request, 'omp/admin_prefs.html', context=context_dict)


@login_required(login_url="/omp/login/")
def edit_category(request, category_name_slug, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    context_dict['confirm_message'] = ""
    context_dict['itemname'] = "Category"

    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype

    # Get category object to edit
    category = Category.objects.get(slug=category_name_slug)
    # Retrieve instance to edit via form
    instance = get_object_or_404(Category, id=category.id)

    form = CategoryForm(initial={'name': category.name})

    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # A HTTP POST?
    if request.method == 'POST':

        form = CategoryForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            context_dict['confirm_message'] = "Category Saved."

        return redirect('omp.views.category_list', username)

    return render(request, 'omp/edit_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def edit_project(request, project_name_slug, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    context_dict['itemname'] = "Project"

    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype

    # Get project object to edit
    project = Project.objects.get(slug=project_name_slug)
    # Retrieve instance to edit via form
    instance = get_object_or_404(Project, id=project.id)

    form = ProjectForm(initial={'name': project.name, 'description': project.description,
                                'softEng': project.softEng, 'category': project.category,
                                'supervisor': project.supervisor})

    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # A HTTP POST?
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect('omp.views.project_list', username)

    return render(request, 'omp/edit_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def edit_student(request, student_name, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    context_dict['itemname'] = "Student"

    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype

    # Get Student object to edit
    student = Student.objects.get(user__username=student_name)
    # Retrieve instance to edit via form
    instance = get_object_or_404(Student, id=student.id)

    form = StudentForm(initial={'user': student.user, 'softEng': student.softEng,
                                'project': student.project, 'category': student.category,
                                'favourites': student.favourites.all(),})

    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # A HTTP POST?
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect('omp.views.student_list', username)

    return render(request, 'omp/edit_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def edit_supervisor(request, supervisor_name, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    context_dict['itemname'] = "Supervisor"

    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype

    # Get Student object to edit
    supervisor = Supervisor.objects.get(user__username=supervisor_name)
    # Retrieve instance to edit via form
    instance = get_object_or_404(Supervisor, id=supervisor.id)

    form = StudentForm(initial={'User': supervisor.user, 'category': supervisor.category,
                                'capacity': supervisor.capacity, 'assigned': supervisor.assigned,})

    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # A HTTP POST?
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect('omp.views.supervisor_list', username)

    return render(request, 'omp/edit_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def edit_administrator(request, admin_name, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    context_dict['itemname'] = "Administrator"

    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype

    # Get Student object to edit
    admin = Administrator.objects.get(user__username=admin_name)
    # Retrieve instance to edit via form
    instance = get_object_or_404(Supervisor, id=admin.id)

    form = AdminForm(initial={'User': admin.user})

    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # A HTTP POST?
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect('omp.views.admin_list', username)

    return render(request, 'omp/edit_generic.html', context=context_dict)


@login_required(login_url="/omp/login/")
def edit_preflist(request, preflist_name, username):
    # kick users with insufficient permissions
    if request.session["permission"] != "Administrator":
        return HttpResponseForbidden()

    context_dict = {}
    context_dict['itemname'] = "Preference List"

    user = request.user
    context_dict['user'] = user

    permission = request.session['permission'].lower()
    usertype = getuserobject(request)
    context_dict[permission] = usertype

    # Get Student object to edit
    preflist = PrefListEntry.objects.get(student__user__username=preflist_name)
    # Retrieve instance to edit via form
    instance = get_object_or_404(PrefListEntry, id=PrefListEntry.id)

    form = StudentForm(initial={'User': preflist.user, 'project': preflist.category,
                                'rank': preflist.rank})

    context_dict['form'] = form
    context_dict['form_errors'] = form.errors

    # A HTTP POST?
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save(commit=True)
            return redirect('omp.views.preference_list', username)

    return render(request, 'omp/edit_generic.html', context=context_dict)



