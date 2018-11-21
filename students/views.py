from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.views.generic import CreateView

from students.models import Student, Course


# noinspection SqlNoDataSourceInspection
def index(request):
    username = request.user
    #Selects classes taken by logged in student
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

def add_class(request):
    if request.method == 'POST':
        username = request.user
        user_id = Student.objects.raw('''SELECT id
                                                FROM students_student
                                                WHERE name == %s''', [str(username)])
        class_name = request.POST['class']
        class_id = Course.objects.raw('''SELECT id
                                    FROM students_course
                                    WHERE name == %s''', [str(class_name)])

        # if not class_id:
        #     return render(request, 'students/index.html', {
        #         'error': 'Class does not exist.'
        #     })
        for item in class_id:
            class_id_int = item.id
        for item in user_id:
            user_id_int = item.id
        # my_prereqs = Student.objects.raw('''SELECT students_course_prereqs.to_course_id as id
        #                                      FROM students_course
        #                                      INNER JOIN students_student_courses
        #                                      ON students_course.id = students_student_courses.course_id
        #                                      INNER JOIN students_student
        #                                      ON students_student_courses.student_id = students_student.id
        #                                      INNER JOIN students_course_prereqs
        #                                      ON students_course_prereqs.from_course_id = students_course.id
        #                                      WHERE students_student.name == %s
        #                                      AND students_course_prereqs.from_course_id = %d''',
        #                                     [str(username), int(class_id_int)])
        # class_prereqs = Course.objects.raw('''SELECT students_course_prereqs.to_course_id as id
        #                                      FROM students_course
        #                                      INNER JOIN students_course_prereqs
        #                                      ON students_course_prereqs.from_course_id = students_course.id
        #                                      WHERE students_course_prereqs.from_course_id = %d''',
        #                                    [int(class_id_int)])
        # print(my_prereqs)
        # print(class_prereqs)
        # my_prereqs_list = []
        # print("@@@@@@@")
        # for item in my_prereqs:
        #     #my_prereqs_list.append(item.)
        #     print(item.id)
        # print(my_prereqs_list)
        # class_prereqs_list = []
        # for item in class_prereqs:
        #     class_prereqs_list.append(item.name)
        #
        # print(class_prereqs_list)
        # if not set(my_prereqs_list)==set(class_prereqs_list):
        #     return render(request, 'students/index.html', {
        #         'error': 'Prereqs not satisfied.'
        #     })
        Student.objects.raw('''INSERT INTO students_student_courses (student_id, course_id)
                                        VALUES (%d, %d)''', [int(user_id_int), int(class_id_int)])
        print(user_id_int, class_id_int)
        print("success")
    return redirect('index',)



def login(request):
    return render(request, 'students/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'students/index.html')
