import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'tango_with_django_project.settings')

import django
django.setup()
from omp.models import User, Project

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    level_3 = [
        {"id": 10, "name": "Level 3 Project 1", "description": "First test project", "softeng": True,},
        {"id": 11, "name": "Level 3 Project 2", "description": "Second test project", "softeng": False},
        {"id": 12, "name": "Level 3 Project 3", "description": "Third test project", "softeng": False},
        {"id": 13, "name": "Level 3 Project4", "description": "Fourth test project", "softeng": True},
        ]
    level_4 = [
        {"id": 1, "name": "Level 4 Project 1", "description": "First test project", "softeng": True,},
        {"id": 2, "name": "Level 4 Project 2", "description": "Second test project", "softeng": False},
        {"id": 3, "name": "Level 4 Project 3", "description": "Third test project", "softeng": False},
        {"id": 4, "name": "Level 4 Project 4", "description": "Fourth test project", "softeng": True},
    ]

    cats = {"Level 3": {"projects": level_3},
        "Level 4": {"projects": level_4}, }


    # If you want to add more catergories or projects,
    # add them to the dictionaries above.
    #The code below goes through the cats dictionary, then adds each category,
    #and then adds all the associated projects for that category.
    cat_counter=1
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_counter)
        cat_counter +=1
        for p in cat_data["pages"]:
            add_project(c, p["id"], p["name"], p["desc"], p["softeng"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_project(cat, id, name, desc, soft):
    p = Page.objects.get_or_create(category=cat, id=id)[0]
    p.name=name
    p.desc=desc
    p.softeng=soft
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