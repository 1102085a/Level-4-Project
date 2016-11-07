from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128, unique = True)
    slug = models.SlugField(unique = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.id


class Project(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    softeng = models.BooleanField(default=False)
    category = models.ForeignKey(Category, default="None")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.id)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.id


class Student(models.Model):
    user = models.ForeignKey(User)
    id = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(Project, default='None')
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.id


class Supervisor(models.Model):
    user = models.ForeignKey(User)
    id = models.CharField(max_length=20, primary_key=True)
    project = models.ForeignKey(Project)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.id


class Administrator(models.Model):
    user = models.ForeignKey(User)
    id = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.id




