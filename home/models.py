from pyexpat import model
from re import L
from turtle import ondrag
from django.db import models
import os

class University(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"

class Field(models.Model):
    name = models.CharField(max_length=200)
    degree = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, blank=True)
    root_link = models.URLField()
    link = models.URLField(blank=True)
    file = models.FileField(upload_to='sheets/', blank=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.slug
    
    def filename(self):
        return os.path.basename(self.file.name)

class Group(models.Model):
    name = models.CharField(max_length=100)
    fields = models.ManyToManyField(Field)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    University = models.ForeignKey(University, on_delete=models.CASCADE)
    fields = models.ManyToManyField(Field)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Faculties"