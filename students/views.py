from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.db import connections,transaction


# Create your views here.
from django.shortcuts import render
from django.views.generic import CreateView

from students.forms import JobForm
from students.models import Student, Course, Job


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
    rows = Course.objects.raw('''SELECT students_course.id, students_course.name, difficulty, skills
                        FROM students_course
                        ORDER BY students_course.name''')

    filtered_complete = None
    filtered_by = None
    if request.method == 'POST':
        gpa = request.POST['gpa']
        skills = request.POST['skills']
        if gpa:
            filtered = Course.objects.raw('''SELECT students_course.id, students_course.name, difficulty, skills
                                                    FROM students_course
                                                    WHERE difficulty >= %s''', [gpa])
            filtered_by = 'GPA >=' + gpa
            class_professor_list = []
            for course in filtered:
                course_professors = Course.objects.raw('''SELECT students_professor.id, students_professor.name
                                                            FROM students_professor_courses
                                                            JOIN students_professor
                                                            ON students_professor_courses.professor_id = students_professor.id
                                                            WHERE students_professor_courses.course_id = %s''',
                                                       [str(course.id)])
                courses = []
                for professor in course_professors:
                    courses.append(professor.name)
                class_professor_list.append(", ".join(courses))
            filtered_complete = list(zip(filtered, class_professor_list))

        if skills:
            filtered = Course.objects.filter(skills__icontains=skills)
            filtered_by = 'Skills = ' + skills
            class_professor_list=[]
            for course in filtered:
                course_professors = Course.objects.raw('''SELECT students_professor.id, students_professor.name
                                                                       FROM students_professor_courses
                                                                       JOIN students_professor
                                                                       ON students_professor_courses.professor_id = students_professor.id
                                                                       WHERE students_professor_courses.course_id = %s''',
                                                       [str(course.id)])
                courses = []
                for professor in course_professors:
                    courses.append(professor.name)
                class_professor_list.append(", ".join(courses))
            filtered_complete = list(zip(filtered, class_professor_list))

    class_professor_list = []
    for course in rows:
        course_professors = Course.objects.raw('''SELECT students_professor.id, students_professor.name
                                                FROM students_professor_courses
                                                JOIN students_professor
                                                ON students_professor_courses.professor_id = students_professor.id
                                                WHERE students_professor_courses.course_id = %s''', [str(course.id)])
        courses = []
        for professor in course_professors:
            courses.append(professor.name)
        class_professor_list.append(", ".join(courses))
    all_courses_complete = list(zip(rows, class_professor_list))
    return render(request, 'students/index.html', {
        'my_courses': my_courses,
        'allCourse': all_courses_complete,
        'filtered': filtered_complete,
        'filtered_by': filtered_by
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

        if not class_id:
            return render(request, 'students/index.html', {
                'error': 'Class does not exist.'
            })
        for item in class_id:
            class_id_int = item.id
        for item in user_id:
            user_id_int = item.id
        my_courses = Student.objects.raw('''SELECT *
                                             FROM students_course 
                                             INNER JOIN students_student_courses
                                             ON students_course.id = students_student_courses.course_id
                                             INNER JOIN students_student
                                             ON students_student_courses.student_id = students_student.id
                                             WHERE students_student.name == %s''', [str(username)])

        class_prereqs = Course.objects.raw('''SELECT *
                                             FROM students_course
                                             INNER JOIN students_course_prereqs
                                             ON students_course_prereqs.from_course_id = students_course.id
                                             WHERE students_course_prereqs.from_course_id = %s''',
                                           [class_id_int])
        my_courses_list = []
        for item in my_courses:
            my_courses_list.append(item.id)
            print(item.id)
        print("@@@")
        class_prereqs_list = []
        for item in class_prereqs:
            class_prereqs_list.append(item.to_course_id)
            print(item.to_course_id)

        print("class prereqs")
        print(class_name)
        print("my classes")
        print(set(my_courses_list))
        if class_id_int in set(my_courses_list):
            return render(request, 'students/index.html', {
                'error': 'Already enrolled in course.'
            })
        if not set(class_prereqs_list).issubset(set(my_courses_list)):
            return render(request, 'students/index.html', {
                'error': 'Prereqs not satisfied.'
            })

        cursor = connections['default'].cursor()

        cursor.execute('''INSERT INTO students_student_courses(student_id, course_id)
                                        VALUES (%s, %s)''', [user_id_int, class_id_int])


    return redirect('index',)

def deleteClass(request):
    if request.method == 'POST':
        username = request.user
        user_id = Student.objects.raw('''SELECT id
                                        FROM students_student
                                        WHERE name == %s''', [str(username)])
        class_name = request.POST['class']
        class_id = Course.objects.raw('''SELECT id
                                            FROM students_course
                                            WHERE name == %s''', [str(class_name)])
        cursor = connections['default'].cursor()
        for item in class_id:
            class_id_int = item.id
        for item in user_id:
            user_id_int = item.id
        cursor.execute('''DELETE FROM students_student_courses
                                           WHERE students_student_courses.student_id = %s AND  
                                           students_student_courses.course_id = %s''', [user_id_int, class_id_int])
    return redirect('index',)
def login(request):
    return render(request, 'students/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'students/index.html')

def jobs(request):
    all_jobs = Job.objects.raw('''SELECT *
                        FROM students_job''')
    form = JobForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/students/jobs')

    job_class_list = []
    for job in all_jobs:
        job_courses = Course.objects.raw('''SELECT *
                                            FROM students_job_courses
                                            JOIN students_course
                                            ON students_job_courses.course_id = students_course.id
                                            WHERE students_job_courses.job_id = %s''', [str(job.id)])
        courses = []
        for course in job_courses:
            courses.append(course.name)
        job_class_list.append(", ".join(courses))
    all_jobs_complete = list(zip(all_jobs, job_class_list))
    return render(request, 'students/jobs.html', {
        'all_jobs': all_jobs_complete,
        'job_form':form
    })
