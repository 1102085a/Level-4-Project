import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectallocationapp.settings')

import django
django.setup()
from omp.models import User, Project, Category, Student, Supervisor, Administrator, PrefListEntry, SiteConfiguration


def populate():
    # First, we instantiate the site configuration model
    sc = SiteConfiguration.objects.get_or_create()[0]
    sc.save()

    # add users
    # username, password, email(optional)
    a = add_user("JohnSmith", "wingdings")
    b = add_user("Richard Spencer", "batman")
    c = add_user("JackDee", "fishnchips")
    d = add_user("BobDylan", "superman")
    e = add_user("RobertSmith", "alligator")
    f = add_user("AdamSys", "iamthemcu")
    x = add_user("DummySupervisor", "testprojects")

    dcat = add_cat("Dummy Projects")
    catlist = [dcat]
    z = add_supervisor(x, catlist, 1000)
    dummy = add_project(dcat, "Dummy project", "A placeholder project", True, z)

    dummy_project = [
        {"name": "Dummy project", "description": "Dummy project", "softEng": True,
            "supervisor": z}
    ]

    # categories
    # initialise before supervisors to fix chicken/egg scenario
    cats = {"Level 3": {"projects": dummy_project}, "Level 4": {"projects": dummy_project}, }

    # put returned category objects in a list
    categories = [None]*2
    count = 0
    for cat, cat_data in cats.items():
        categories[count] = add_cat(cat)
        count += 1

    # Supervisors
    # user, id, project, category, capacity
    # make list of projects to add (many to many field)
    g = add_supervisor(d, categories, 10)
    h = add_supervisor(e, categories, 12)

    # projects
    # name, description, softEng, category, supervisor
    level_3 = [
        {"name": "Level 3 Project 1", "description": "First project", "softEng": True, "supervisor": g},
        {"name": "Level 3 Project 2", "description": "Second project", "softEng": False, "supervisor": h},
        {"name": "Level 3 Project 3", "description": "Third project", "softEng": False, "supervisor": g},
        {"name": "Level 3 Project 4", "description": "Fourth project", "softEng": True, "supervisor": h},
        ]
    level_4 = [
        {"name": "Level 4 Project 2", "description": "Second project", "softEng": True, "supervisor": g},
        {"name": "Level 4 Project 3", "description": "Third project", "softEng": False, "supervisor": h},
        {"name": "Level 4 Project 4", "description": "Fourth project", "softEng": False, "supervisor": h},
        {"name": "Level 4 Project 5", "description": "Fifth project", "softEng": True, "supervisor": h},
    ]

    # projects
    # name, description, softEng, category, supervisor
    cats["Level 3"]["projects"] = level_3
    cats["Level 4"]["projects"] = level_4


    # students
    # user, softEng, category,

    sa = add_student(a, False, categories[0], dummy)
    sb = add_student(b, True, categories[1], dummy)
    sc = add_student(c, False, categories[1], dummy)

    # Admins
    # user
    add_admin(f)

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated projects for that category.

    # store projects for preflists in list
    projectlist = []

    for cat, cat_data in cats.items():
        count = 0
        c = categories[count]
        for p in cat_data["projects"]:
            p = add_project(c, p["name"], p["description"], p["softEng"], p["supervisor"])
            projectlist.append(p)

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Project.objects.filter(category=c):
            print("Category- {0}: Added - {1}".format(str(c), str(p)))

    # student preference lists
    # user, project, ranking
    add_preflist(sa, projectlist[4], 1)
    add_preflist(sa, projectlist[6], 2)
    add_preflist(sb, projectlist[3], 1)
    add_preflist(sc, projectlist[2], 1)
    add_preflist(sc, projectlist[3], 2)
    add_preflist(sc, projectlist[1], 3)


def add_user(name, password):
    try:
        user = User.objects.get(username=name)
        print(user.username + " already exists.")
    except User.DoesNotExist:
        print("User added: " + name)
        u = User.objects.create_user(username=name, password=password)
        u.save()
        return u
    return user


def add_student(user, softEng, category, project):
    s = Student.objects.get_or_create(user=user, softEng=softEng, category=category, project=project)[0]
    print("Student added: " + user.username)
    s.save()
    return s


def add_preflist(student, project, ranking):
    pl = PrefListEntry.objects.get_or_create(student=student, project=project, rank=ranking)[0]
    pl.save()


def add_supervisor(user, categories, capacity):
    s = Supervisor.objects.get_or_create(user=user, capacity=capacity)[0]
    for cat in categories:
        s.category.add(cat)
    print("Supervisor added: " + user.username)
    s.save()
    return s


def add_admin(user):
    a = Administrator.objects.get_or_create(user=user)[0]
    print("Administrator added: " + user.username)
    a.save()


def add_project(cat, name, desc, softeng, supervisor):
    p = Project.objects.get_or_create(category=cat, name=name,
                                        description=desc, softEng=softeng, supervisor=supervisor)[0]
    p.save()
    return p


def add_cat(name,):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    django.setup()
    print("Starting OMP population script...")
    populate()
