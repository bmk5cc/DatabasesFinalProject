from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from students.models import Student, Course


# noinspection SqlNoDataSourceInspection
def index(request):
    username = request.user
    my_courses = Student.objects.raw('''SELECT *
                                     FROM students_course 
                                     INNER JOIN students_student_courses
                                     ON students_course.id = students_student_courses.course_id
                                     INNER JOIN students_student
                                     ON students_student_courses.student_id = students_student.id
                                     WHERE students_student.name == %s''', [str(username)])
    return render(request, 'students/index.html', {
        'my_courses': my_courses,
    })

def login(request):
    return render(request, 'students/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'students/index.html')
