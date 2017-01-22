from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Optimal Matching Portal')
    maintenance_mode = models.BooleanField(default=False)
    site_stage = models.BooleanField(default=1)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


class Category(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    softEng = models.BooleanField(default=False)
    category = models.ForeignKey(Category, default="None")
    supervisor = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User)
    id = models.CharField(max_length=20, primary_key=True)
    softEng = models.BooleanField(default=False)
    project = models.ForeignKey(Project, default='None', related_name='assigned_project', null=True)
    category = models.ForeignKey(Category)
    favourites = models.ManyToManyField(Project, blank=True, related_name='favourite_projects')
    preference_list = models.ManyToManyField(Project, blank=True, through='PrefListEntry',
                                             related_name='ranked_projects')

    def __str__(self):
        return self.id


class PrefListEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rank = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Preference Lists'

    def __str__(self):
        name = str(self.student.id) + " pref " + str(self.rank)
        return name


class Supervisor(models.Model):
    user = models.ForeignKey(User)
    id = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(Project)
    category = models.ManyToManyField(Category)
    capacity = models.IntegerField()

    def __str__(self):
        return self.id


class Administrator(models.Model):
    user = models.ForeignKey(User)

    def __str__(self):
        return self.id




