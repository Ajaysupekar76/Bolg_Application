# Generated by Django 5.1.1 on 2024-10-21 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0018_education_employee_delete_employees_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='Employees',
        ),
    ]
