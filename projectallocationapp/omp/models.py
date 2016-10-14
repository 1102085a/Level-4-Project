from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128)
    studentAccess = models.BooleanField(default=False)
    supervisorAccess = models.BooleanField(default=False)
    adminAccess = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128, unique = True)

    def __str__(self):
        return self.id


class Project(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    softeng = models.BooleanField(default=False)

    def __str__(self):
        return self.id

class Student(models.Model):
    studentID = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    project = models.OneToOneField(Project)
    category = models.OneToOneField(Category)

    def __str__(self):
        return self.name

class Supervisor(models.Model):
    supervisorID = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    project = models.ForeignKey(Project)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Administrator(models.Model):
    adminID = models.ForeignKey(User)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


