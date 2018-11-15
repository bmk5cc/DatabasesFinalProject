from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=128, null=False)
    major = models.CharField(max_length=128, null=False)
    year = models.IntegerField(null=False)
    gpa = models.DecimalField(decimal_places=2, max_digits=3)
    departments = models.ManyToManyField('Department')
    courses = models.ManyToManyField('Course')

class Professor(models.Model):
    name = models.CharField(max_length=128, null=False)
    rating = models.IntegerField(null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    courses = models.ManyToManyField('Course')

class Job(models.Model):
    title = models.CharField(max_length=128, null=False)
    company = models.CharField(max_length=128, null=False)
    courses = models.ManyToManyField('Course')

class Course(models.Model):
    name = models.CharField(max_length=128, null=False)
    major = models.CharField(max_length=128, null=False)
    difficulty = models.CharField(max_length=128, null=False)
    skills = models.CharField(max_length=128, null=False)

class Department(models.Model):
    name = models.CharField(max_length=128, null=False)
