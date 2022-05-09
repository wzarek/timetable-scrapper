from turtle import ondrag
from django.db import models

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
    degree = models.CharField(max_length=100)
    year = models.IntegerField()
    type = models.CharField(max_length=50)
    root_link = models.URLField()
    link = models.URLField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name
