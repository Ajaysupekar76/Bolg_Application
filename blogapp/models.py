from django.db import models

class UserRegister(models.Model):
    """User model for registration."""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    def __str__(self):
        return self.name


from django.db import models
class BlogCategory(models.Model):
    # Fields with integer representation for 0 and 1
    STATUS_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    DELETED_STATUS = (
        (0, 'Not Deleted'),
        (1, 'Deleted'),
    )
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)  # Associate with User
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')
    is_deleted = models.IntegerField(choices=DELETED_STATUS, default=0)  # 0 for Not Deleted
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)  # 1 for Active
    is_created = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    is_updated = models.DateTimeField(auto_now=True)  # Automatically set to now when updated
    def __str__(self):
        return self.name


from django.db import models  # Import Django models
from .models import BlogCategory, UserRegister  # Import your custom models from the current app's models.py
class Blog(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)  # Associate with User
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=False)
    catogiry_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import json

class Emps(models.Model):
    STATUS_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    DELETED_STATUS = (
        (0, 'Not Deleted'),
        (1, 'Deleted'),
    )
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)  
    address = models.TextField()
    country = models.CharField(max_length=100)  
    state = models.CharField(max_length=100) 
    city = models.CharField(max_length=100)  
    pincode = models.CharField(max_length=10)
    education_details = models.JSONField(default=dict)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    deleted_status = models.IntegerField(choices=DELETED_STATUS, default=0)
    is_updated = models.DateTimeField(auto_now=True)

   


    def __str__(self):
        return self.full_name

   