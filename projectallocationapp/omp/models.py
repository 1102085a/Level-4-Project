from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=255, default='Optimal Matching Portal')
    maintenance_mode = models.BooleanField(default=False)
    site_stage = models.IntegerField(default=1)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Supervisor(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    category = models.ManyToManyField(Category)
    capacity = models.IntegerField(default=1)
    assigned = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000)
    softEng = models.BooleanField(default=False)
    category = models.ForeignKey(Category, default=None)
    supervisor = models.ForeignKey(Supervisor, blank=True, null=True)
    assigned = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User)
    softEng = models.BooleanField(default=False)
    project = models.ForeignKey(Project, default='None', related_name='assigned_project', null=True, blank=True)
    category = models.ForeignKey(Category)
    favourites = models.ManyToManyField(Project, blank=True, related_name='favourite_projects')
    preference_list = models.ManyToManyField(Project, blank=True, through='PrefListEntry',
                                             related_name='ranked_projects')

    def __str__(self):
        return self.user.username


class PrefListEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rank = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Preference Lists'

    def __str__(self):
        name = str(self.student.user.username) + " - Rank: " + str(self.rank)
        return name


class Administrator(models.Model):
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.username




