from django.contrib import admin

# Register your models here.
from .models import Student,Professor,Job,Course,Department



class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','year']

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ["name"]

class JobAdmin(admin.ModelAdmin):
    list_display = ["title"]

class CourseAdmin(admin.ModelAdmin):
    list_display = ["name"]

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(Student,StudentAdmin)

admin.site.register(Professor,ProfessorAdmin)

admin.site.register(Job,JobAdmin)

admin.site.register(Course,CourseAdmin)

admin.site.register(Department,DepartmentAdmin)
