# Generated by Django 2.1.2 on 2018-11-19 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20181114_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='prereqs',
            field=models.ManyToManyField(related_name='_course_prereqs_+', to='students.Course'),
        ),
    ]
