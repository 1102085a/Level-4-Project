import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'projectallocationapp.settings')

import django
django.setup()
from omp.models import User, Project, Category, Student

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    students = [
        {"id": 1, "name": "John Smith"},
        {"id": 2, "name": "Richard Spence"},
        {"id": 3, "name": "Jack Dee"},
        {"id": 4, "name": "Bob Dylan"}

    ]

    level_3 = [
        {"id": 10, "name": "Level 3 Project 1", "description": "First test project", "softeng": True,},
        {"id": 11, "name": "Level 3 Project 2", "description": "Second test project", "softeng": False},
        {"id": 12, "name": "Level 3 Project 3", "description": "Third test project", "softeng": False},
        {"id": 13, "name": "Level 3 Project 4", "description": "Fourth test project", "softeng": True},
        ]
    level_4 = [
        {"id": 2, "name": "Level 4 Project 2", "description": "Second test project", "softeng": True,},
        {"id": 3, "name": "Level 4 Project 3", "description": "Third test project", "softeng": False},
        {"id": 4, "name": "Level 4 Project 4", "description": "Fourth test project", "softeng": False},
        {"id": 5, "name": "Level 4 Project 5", "description": "Fifth test project", "softeng": True},
    ]

    cats = {"Level 3": {"projects": level_3},
        "Level 4": {"projects": level_4}, }

    users = {"students": {"users": students}}


    # If you want to add more users, catergories or projects,
    # add them to the dictionaries above.
    #The code below goes through the cats dictionary, then adds each category,
    #and then adds all the associated projects for that category.

    #for user, user_data in users.items():
     #   for s in user_data["users"]:
      #      add_user(s["id"], s["name"])
       #     add_student(s["id"], s["name"])

    # Print out the users we have added.
    #for u in User.objects.all():
     #       print("- {0}".format(str(u)))

    cat_counter=1
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_counter)
        cat_counter +=1
        for p in cat_data["projects"]:
            add_project(c, p["id"], p["name"], p["description"], p["softeng"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Project.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_user(id, name):
    u = User.objects.get_or_create(id=id, name=name)[0]
    u.student_access = True
    u.student_access = False
    u.student_access = False


def add_student(id, name):
    s = Student.objects.get_or_create(id=id, name=name)[0]
    s.project = "None"
    s.category = "Level 4"

def add_project(cat, id, name, desc, soft):
    p = Project.objects.get_or_create(category=cat, id=id)[0]
    p.name = name
    p.desc = desc
    p.softeng = soft
    p.save()
    return p

def add_cat(name, id):
    c = Category.objects.get_or_create(id=id, name=name)[0]
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting OMP population script...")
    populate()