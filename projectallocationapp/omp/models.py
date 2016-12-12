from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    catid = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.catid)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.id


class Project(models.Model):
    proid = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    softeng = models.BooleanField(default=False)
    category = models.ForeignKey(Category, default="None")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.proid)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.id


class Student(models.Model):
    user = models.ForeignKey(User)
    stuid = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(Project, default='None', related_name='assigned_project')
    category = models.ForeignKey(Category)
    favourites = models.ManyToManyField(Project, blank=True, related_name='favourite_projects')

    def __str__(self):
        return self.id


class Preferences(models.Model):
    project = models.ManyToManyField(Project)
    student = models.ManyToManyField(Student)
    ranking = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.id


class Supervisor(models.Model):
    user = models.ForeignKey(User)
    supid = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(Project)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.id


class Administrator(models.Model):
    user = models.ForeignKey(User)
    adid = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.id




