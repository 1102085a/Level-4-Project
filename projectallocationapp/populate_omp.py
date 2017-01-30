import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectallocationapp.settings')

import django
django.setup()
from omp.models import User, Project, Category, Student, Supervisor, Administrator, PrefListEntry


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    # add users
    # username, password, email(optional)
    a = add_user("John Smith", "wingdings")
    b = add_user("Richard Spencer", "batman")
    c = add_user("Jack Dee", "fishnchips")
    d = add_user("Bob Dylan", "superman")
    e = add_user("Robert Smith", "alligator")
    f = add_user("Adam Sys", "iamthemcu")

    # categories
    cats = {"Level 3": {"projects": None}, "Level 4": {"projects": None}, }

    # put returned category objects in a list
    categories = [None]*2
    count = 0
    for cat, cat_data in cats.items():
        categories[count] = add_cat(cat)
        count += 1

    # Supervisors
    # user, id, project, category, capacity
    # make list of projects to add (many to many field)
    add_supervisor(d, categories, 10)
    add_supervisor(e, categories, 12)

    # projects
    # name, description, softEng, category, supervisor
    level_3 = [
        {"name": "Level 3 Project 1", "description": "First project", "softEng": True, "supervisor": d},
        {"name": "Level 3 Project 2", "description": "Second project", "softEng": False, "supervisor": e},
        {"name": "Level 3 Project 3", "description": "Third project", "softEng": False, "supervisor": d},
        {"name": "Level 3 Project 4", "description": "Fourth project", "softEng": True, "supervisor": e},
        ]
    level_4 = [
        {"name": "Level 4 Project 2", "description": "Second project", "softEng": True, "creator": "Bob Dylan"},
        {"name": "Level 4 Project 3", "description": "Third project", "softEng": False, "creator": "Robert Smith"},
        {"name": "Level 4 Project 4", "description": "Fourth project", "softEng": False, "creator": "Robert Smith"},
        {"name": "Level 4 Project 5", "description": "Fifth project", "softEng": True, "creator": "Robert Smith"},
    ]

    # projects
    # name, description, softEng, category, supervisor
    cats["Level 3"]["projects"] = level_3
    cats["Level 4"]["projects"] = level_4

    # students
    # user, softEng, category,
    sa = add_student(a, False, categories[0])
    sb = add_student(b, True, categories[1])
    sc = add_student(c, False, categories[1])

    # student preference lists
    # user, project, ranking
    add_preflist(sa, level_3[0], 1)
    add_preflist(sa, level_3[2], 2)
    add_preflist(sb, level_4[3], 1)
    add_preflist(sc, level_4[2], 1)
    add_preflist(sc, level_4[3], 2)
    add_preflist(sc, level_4[1], 3)



    # Admins
    # user
    add_admin(f)

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated projects for that category.

    for cat, cat_data in cats.items():
        for p in cat_data["projects"]:
            add_project(c, p["id"], p["name"], p["description"], p["softeng"], p["supervisor"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Project.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_user(name, password):
    try:
        user = User.objects.get(username=name)
        print(user.username + " already exists.")
    except User.DoesNotExist:
        print(name + " doesn't exist, creating...")
        u = User.objects.create_user(username=name, password=password)
        u.save()
        return u
    return user


def add_student(user, id, softEng, category):
    s = Student.objects.get_or_create()[0]
    s.user = user
    s.id = id
    s.softEng = softEng
    s.category = category
    s.save()
    return s


def add_preflist(student, project, ranking):
    pl = PrefListEntry.objects.get_or_create(student=student, project=project, ranking=ranking)[0]
    pl.save()


def add_supervisor(user, id, categories, capacity):
    s = Supervisor.objects.get_or_create(user=user, id=id, capacity=capacity)[0]
    s.save()
    for cat in categories:
        s.category.add(cat)


def add_admin(user):
    a = Administrator.objects.get_or_create(user=user)[0]
    a.save()


def add_project(cat, id, name, desc, softeng, supervisor):
    p = Project.objects.get_or_create(category=cat, id=id, name=name,
                                        desc=desc,softEng=softeng, supervisor=supervisor)[0]
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
