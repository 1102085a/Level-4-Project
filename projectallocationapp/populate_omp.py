import os
import django
from omp.models import User, Project, Category, Student, Administrator




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
    d = add_user("Bob Dylan","superman")
    e = add_user("Robert Smith", "alligator")
    f = add_user("Adam Sys", "iamthemcu")

    # projects
    # name, description, softEng, category, supervisor

    level_3 = [
        {"name": "Level 3 Project 1", "description": "First project", "softEng": True, "supervisor": "Bob Dylan"},
        {"name": "Level 3 Project 2", "description": "Second project", "softEng": False, "supervisor": "Robert Smith"},
        {"name": "Level 3 Project 3", "description": "Third project", "softEng": False, "supervisor": "Bob Dylan"},
        {"name": "Level 3 Project 4", "description": "Fourth project", "softEng": True, "supervisor": "Robert Smith"},
        ]
    level_4 = [
        {"name": "Level 4 Project 2", "description": "Second project", "softEng": True, "supervisor": "Bob Dylan"},
        {"name": "Level 4 Project 3", "description": "Third project", "softEng": False, "supervisor": "Robert Smith"},
        {"name": "Level 4 Project 4", "description": "Fourth project", "softEng": False, "supervisor": "Robert Smith"},
        {"name": "Level 4 Project 5", "description": "Fifth project", "softEng": True, "supervisor": "Robert Smith"},
    ]

    cats = {"Level 3": {"projects": level_3}, "Level 4": {"projects": level_4}, }

    # students
    # user, id, softEng, category,
    add_student(a, a.name, False, cats["Level 3"])
    add_student(b, b.name, True, cats["Level 4"])
    add_student(c, c.name, False, cats["Level 4"])

    # Supervisors
    # user, id, project, category, capacity
    projects_bob = [level_3[0], level_3[2], level_4[0]]
    projects_rob = [level_3[1], level_3[3], level_4[1], level_4[2], level_4[3]]
    add_supervisor(d, d.name, projects_bob, [cats["Level 4"]], 10)
    add_supervisor(e, e.name, projects_rob, [cats["Level 3"], cats["Level 4"]], 12)

    # Admins
    # user
    add_admin(f)

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated projects for that category.

    cat_counter = 1
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_counter)
        cat_counter += 1
        for p in cat_data["projects"]:
            add_project(c, p["id"], p["name"], p["description"], p["softeng"], p["supervisor"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Project.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_user(name, password):
    u = User.objects.get_or_create(name=name, password=password)[0]
    u.save()
    return u


def add_student(user, id, softEng, category):
    s = Student.objects.get_or_create(user=user, id=id, softEng=softEng, category=category)[0]
    s.save()


def add_supervisor(user, id, projects, category, capacity):
    s = Student.objects.get_or_create(user=user, id=id, capacity=capacity)
    s.save()
    for project in projects:
        s.add(project)
    for cat in category:
        s.add(cat)


def add_admin(user):
    a = Administrator.objects.get_or_create(user=user)
    a.save()


def add_project(cat, id, name, desc, softeng, supervisor):
    p = Project.objects.get_or_create(category=cat, id=id, name=name,
                                        desc=desc,softEng=softeng, supervisor=supervisor)[0]
    p.save()
    return p


def add_cat(name, id):
    c = Category.objects.get_or_create(id=id, name=name)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting OMP population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'projectallocationapp.settings')
    django.setup()
    populate()
