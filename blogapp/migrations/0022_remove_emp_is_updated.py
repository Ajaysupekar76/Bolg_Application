# Generated by Django 5.1.1 on 2024-10-21 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0021_emp_delete_education_delete_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emp',
            name='is_updated',
        ),
    ]
