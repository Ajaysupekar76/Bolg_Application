from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from random import randint
import json
from .models import UserRegister, Blog  # Ensure this is the correct import for your User model



def RegisterPage(request):
    return render(request,"register.html")

from .models import UserRegister  # Make sure to import your UserRegister model
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the email already exists
        if UserRegister.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return render(request, 'register.html', {'name': name, 'email': email})

        try:
            # Create and save the user only if validations pass
            user_profile = UserRegister(
                name=name,
                email=email,
                password=password,  # Ideally, hash the password before saving
            )
            user_profile.save()
            # Instead of redirecting immediately, pass a flag to trigger the popup
            return render(request, 'register.html', {'registration_success': True})
        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'register.html', {'name': name, 'email': email})

    return render(request, 'register.html')



def LoginPage(request):
    return render(request, "login.html")

def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        if not UserRegister.objects.filter(email=email).exists():
            messages.error(request, "Email does not exist.")
            return render(request, 'login.html', { 'email': email})

        try:
            user = UserRegister.objects.get(email=email)
            
            if user.password == password:  # You should hash and verify passwords securely in production.
                # Set session data for the logged-in user
                request.session['user_id'] = user.id  # Store user ID in session
                request.session['name'] = user.name
                request.session['email'] = user.email
                request.session['login_success'] = True  # Set login success flag
                return redirect('addblog')  # Redirect to the login page to trigger success alert
            else:
                messages.error(request, 'Password does not match!')
                return redirect('loginpage')
        except UserRegister.DoesNotExist:
            messages.error(request, 'User does not exist!')
            return redirect('loginpage')
    return render(request, 'login.html')




def LogOut(request):
    del request.session['email']
    del request.session['name']
    del request.session['user_id']
    return redirect('loginpage')

def ForgotPage(request):
    return render(request,"forgot.html")
    
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        # Check if the email exists in the database
        user_exists = UserRegister.objects.filter(email=email).exists()
        if not user_exists:
            return JsonResponse({'success': False, 'message': 'Email does not exist.'})
        otp = randint(100000, 999999)
        try:
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is {otp}',
                'ajaysupekar76@gmail.com',  # Replace with your sender email
                [email],
                fail_silently=False,
            )
            # Store OTP in session for later verification
            request.session['email_otp'] = otp
            request.session['register_email'] = email
            return JsonResponse({'success': True, 'message': 'OTP sent successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def ResetPassword(request):
    email = request.session.get('register_email')  # Get email from session instead
    if not email:
        return redirect('forgotpage')  # Redirect if no email is found in session
    user = get_object_or_404(UserRegister, email=email)
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        try:
            user.password = new_password  # Ensure password hashing here
            user.save()  # Save the updated user object to the database
            #messages.success(request, 'Password reset successfully.')
            return render(request, 'forgot.html', {'forgot_success': True})

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('forgotpage')
    return render(request, 'forgotpage')

def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_otp = int(data.get('otp'))
        stored_otp = request.session.get('email_otp')

        if stored_otp and entered_otp == stored_otp:
            # Store the email in session to be used for resetting password
            return JsonResponse({'success': True, 'message': 'OTP verified successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid OTP.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


########################### Blog CURD operation ####################

def BlogPage(request):
    return render(request,"blog.html")



from django.core.files.storage import FileSystemStorage
from .models import Blog, BlogCategory, UserRegister
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
def fetch_categories(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User not logged in'}, status=401)
    user = get_object_or_404(UserRegister, id=user_id)
    categories = BlogCategory.objects.filter(user=user).values('id', 'name')
    return JsonResponse(list(categories), safe=False)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Blog, BlogCategory, UserRegister

def check_category_in_blog(request):
    category_id = request.GET.get('category_id')
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User not logged in'}, status=401)
    if not category_id:
        return JsonResponse({'error': 'No category selected'}, status=400)
    # Get the user
    user = get_object_or_404(UserRegister, id=user_id)

    # Check if the category is already used in the blog table for that user
    if Blog.objects.filter(user=user, category_id=category_id).exists():
        return JsonResponse({'exists': True, 'message': 'This category is already used in one of your blogs.'})
    else:
        return JsonResponse({'exists': False})





from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import BlogCategory, UserRegister, Blog

def AddBlog(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginpage')
    user = get_object_or_404(UserRegister, id=user_id)
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        author = request.POST.get('author').strip()
        description = request.POST.get('description').strip()
        content = request.POST.get('content').strip()
        category_id = request.POST.get('catogiry_name').strip()  # Form is submitting category ID
        image = request.FILES.get('image')

        print(f"Category ID from Form: {category_id}")  # Debugging line

        # Validate that category_id is valid
        try:
            category = BlogCategory.objects.get(id=category_id, user=user)
        except BlogCategory.DoesNotExist:
            print(f"No category found with ID '{category_id}' for user '{user}'")  # Debugging line
            categories = BlogCategory.objects.filter(user=user, is_deleted=0, status=1)
            return render(request, 'blog.html', {
                'error': 'Category not found. Please select a valid category.',
                'categories': categories
            })
        # Save the category name from the fetched category
        category_name = category.name

        # Create the new blog entry
        blog = Blog(
            user=user, 
            title=title, 
            author=author, 
            description=description, 
            content=content, 
            category=category,  # Save the category as an object
            catogiry_name=category_name  # Save the category name
        )
        # Handle the image upload
        if image:
            blog.image = image  # Store the image directly
        blog.save()  # Save the blog entry
        return render(request, 'blog.html', {'add_success': True})
    # Pass categories to the template
    categories = BlogCategory.objects.filter(user=user, is_deleted=0, status=1)
    return render(request, 'blog.html', {'categories': categories})



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Blog, BlogCategory, UserRegister
def category_exists(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        category_id = request.POST.get('category_id')
        if not user_id:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        user = get_object_or_404(UserRegister, id=user_id)
        # Check if a blog with the selected category already exists for the user
        exists = Blog.objects.filter(user=user, category_id=category_id).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)






def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        image = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(f'uploads/{image.name}', image)
        uploaded_file_url = fs.url(filename)
        return JsonResponse({
            'success': True,
            'url': uploaded_file_url
        })
    return JsonResponse({'success': False, 'error': 'Invalid request.'})


def BlogListPage(request):
    user_id = request.session.get('user_id') 
    if not user_id:
        return redirect('loginpage') 
    # Fetch the user object
    user = get_object_or_404(UserRegister, id=user_id)
    blogs = Blog.objects.filter(user=user)  # Filter blogs by the logged-in user
    return render(request, "bloglist.html", {"blogs": blogs})


def BlogDetailPage(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Fetch the blog by ID
    return render(request, "blog_details.html", {"blog": blog})


import os
import re
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
def DeleteBlog(request, blog_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginpage')  # Redirect to login if user not logged in
    user = get_object_or_404(UserRegister, id=user_id)
    blog = get_object_or_404(Blog, id=blog_id, user=user)

    # Delete the main image associated with the blog (if any)
    if blog.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(blog.image))
        if os.path.exists(image_path):
            os.remove(image_path)
    # Extract and delete any images embedded within the blog's content
    content = blog.content
    image_urls = re.findall(r'<img.*?src="(.*?)"', content)  # Regex to find image URLs in <img> tags

    for image_url in image_urls:
        # Assuming the images are stored under MEDIA_URL
        if image_url.startswith(settings.MEDIA_URL):
            # Get the relative path of the image
            relative_image_path = image_url.replace(settings.MEDIA_URL, '')
            image_path = os.path.join(settings.MEDIA_ROOT, relative_image_path)

            # Delete the image if it exists
            if os.path.exists(image_path):
                os.remove(image_path)
    # Now delete the blog instance from the database
    blog.delete()
    # Redirect to the blog list page
    return redirect('bloglist')


def EditBlog(request, blog_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginpage')  # Redirect to login page if no user is found in session
    user = get_object_or_404(UserRegister, id=user_id)
    blog = get_object_or_404(Blog, id=blog_id, user=user)
    if request.method == 'POST':
        # Update the blog with the new data
        blog.title = request.POST.get('title')
        blog.author = request.POST.get('author')
        blog.description = request.POST.get('description')
        blog.content = request.POST.get('content')
        # Update image if a new one is uploaded
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        blog.save()  # Save the updated blog to the database
        return render(request, 'edit.html', {'blog': blog,'edit_success': True})
    return render(request, 'edit.html', {'blog': blog})  # Pass the blog to the template for pre-filling the form



#########################


# views.py

from .forms import BlogCategoryForm  # Make sure to import your form
from django.http import JsonResponse
from .models import BlogCategory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogCategory
from .forms import BlogCategoryForm
from django.contrib.auth.decorators import login_required

def AddBlogCategory(request):
    # Check if the user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginpage')  # Redirect to login page if no user is found in session
    user = get_object_or_404(UserRegister, id=user_id)  # Get the logged-in user
    if request.method == "POST":
        form = BlogCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            # Check if the category already exists for this user
            if BlogCategory.objects.filter(name=name, user=user).exists():
                return JsonResponse({'success': False, 'exists': True}, status=400)

            # Create a new category instance but don't save it to the database yet
            category = form.save(commit=False)  
            category.user = user  # Assign the logged-in user to the category
            category.save()  # Save the category to the database

            return JsonResponse({'success': True, 'redirect_url': '/catogirylist/'})  # Adjust this URL to your category list page

        # Return validation errors if any
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    # Render the form for GET requests
    form = BlogCategoryForm()
    return render(request, 'addcatogiry.html', {'form': form})




def Check_category_exists(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        exists = BlogCategory.objects.filter(name=category_name).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False}, status=400)  # In case of non-POST requests



from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import BlogCategory
from .models import UserRegister  # Import your user model if needed

def Catogiry_List(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginpage')  # Redirect to login page if no user is found in session
    user = get_object_or_404(UserRegister, id=user_id)  # Get the logged-in user
    # Get only active categories associated with the logged-in user
    categories_list = BlogCategory.objects.filter(user=user, is_deleted=0)  
    paginator = Paginator(categories_list, 5)  # Show 5 categories per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    categories = paginator.get_page(page_number)  # Get the categories for the current page
    return render(request, 'categiry_list.html', {'categories': categories})





from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import BlogCategory  # Adjust the import according to your project structure
from .forms import BlogCategoryForm  # Adjust the import according to your project structure

def UpdateBlogCategory(request, pk):
    category = get_object_or_404(BlogCategory, pk=pk)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect_url': '/catogirylist/'})  # Adjust this URL to your category list page
    else:
        form = BlogCategoryForm(instance=category)
    return render(request, 'update_category.html', {
        'form': form,
        'category': category
    })





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BlogCategory

@csrf_exempt  # This is necessary if you are not using CSRF tokens in AJAX, but it's better to keep it for security
def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        try:
            category = BlogCategory.objects.get(id=category_id)
            category.is_deleted = 1  # Set status to "Deleted"
            category.save()
            return JsonResponse({'success': True, 'message': 'Category deleted successfully.'})
        except BlogCategory.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Category not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



import os
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Emps

def execute_sql_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Executing SQL file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_commands = file.read()
    except UnicodeDecodeError as e:
        print(f"Error reading file {file_path}: {e}")
        return

    with connection.cursor() as cursor:
        for command in sql_commands.split(';'):
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    print(f"Executed command: {command[:50]}...")
                except Exception as e:
                    print(f"Error executing command: {e}")

def check_data_loaded(table_name):
    with connection.cursor() as cursor:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error checking data in {table_name}: {e}")
            return False

def import_sql_files():
    sql_files = {
        "country.sql": "Country",
        "state.sql": "State",
        "cities.sql": "Cities"
    }

    base_path = "C:\\Users\\Ajay\\Desktop\\Blog\\database\\"
    load_status = {}

    for sql_file, table_name in sql_files.items():
        file_path = os.path.join(base_path, sql_file)
        if check_data_loaded(table_name):
            load_status[table_name] = "Data already loaded"
        else:
            execute_sql_file(file_path)
            load_status[table_name] = "Data loaded successfully" if check_data_loaded(table_name) else "Failed to load data"
    
    return load_status

def get_countries():
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM country")
        return [{'name': row[0]} for row in cursor.fetchall()]

def get_states(country_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM state WHERE country_id = (SELECT id FROM country WHERE name = %s)", [country_name])
        return [{'name': row[0]} for row in cursor.fetchall()]

def get_cities(state_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM cities WHERE state_id = (SELECT id FROM state WHERE name = %s)", [state_name])
        return [{'name': row[0]} for row in cursor.fetchall()]

def load_states(request):
    country_name = request.GET.get('country_name')
    states = get_states(country_name)
    return JsonResponse({'states': states})

def load_cities(request):
    state_name = request.GET.get('state_name')
    cities = get_cities(state_name)
    return JsonResponse({'cities': cities})



from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Emps, UserRegister

def AddEmp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginpage')  # Redirect to login page if no user is found in session
    user = get_object_or_404(UserRegister, id=user_id)  # Get the logged-in user
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')

        # Check if email or mobile number already exists
        if Emps.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'addemp.html', {'countries': get_countries(), 'email_error': True})

        # Collect education details
        education_details = []
        course_names = request.POST.getlist('course_name')
        universities = request.POST.getlist('university')
        passing_years = request.POST.getlist('passing_year')
        percentages = request.POST.getlist('percentage')

        for course_name, university, passing_year, percentage in zip(course_names, universities, passing_years, percentages):
            if all([course_name, university, passing_year, percentage]):
                education_details.append({
                    'course_name': course_name,
                    'university': university,
                    'passing_year': passing_year,
                    'percentage': percentage
                })
        # Create an Employee instance
        employee = Emps.objects.create(
            full_name=full_name,
            email=email,
            mobile_number=mobile_number,
            gender=gender,
            address=address,
            country=country,
            state=state,
            city=city,
            pincode=pincode,
            education_details=education_details
        )

        messages.success(request, 'Employee added successfully!')
        return redirect('listemp')
    return render(request, 'addemp.html', {'countries': get_countries(), 'email_error': False})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Emps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Emps


from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Emps, UserRegister
from django.db import connection

def get_countries():
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM country")
        return [{'name': row[0]} for row in cursor.fetchall()]

def get_states(country_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM state WHERE country_id = (SELECT id FROM country WHERE name = %s)", [country_name])
        return [{'name': row[0]} for row in cursor.fetchall()]

def get_cities(state_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM cities WHERE state_id = (SELECT id FROM state WHERE name = %s)", [state_name])
        return [{'name': row[0]} for row in cursor.fetchall()]    

def load_states(request):
    country_name = request.GET.get('country_name')
    states = get_states(country_name)
    return JsonResponse({'states': states})

def load_cities(request):
    state_name = request.GET.get('state_name')
    cities = get_cities(state_name)
    return JsonResponse({'cities': cities})


def UpdateEmp(request, employee_id):
    employee = get_object_or_404(Emps, id=employee_id)
    if request.method == 'POST':
        # Update employee details
        employee.full_name = request.POST.get('full_name')
        employee.email = request.POST.get('email')
        employee.mobile_number = request.POST.get('mobile_number')
        employee.gender = request.POST.get('gender')
        employee.address = request.POST.get('address')
        employee.country = request.POST.get('country')
        employee.state = request.POST.get('state')
        employee.city = request.POST.get('city')
        employee.pincode = request.POST.get('pincode')

        # Collect updated education details
        education_details = []
        course_names = request.POST.getlist('course_name')
        universities = request.POST.getlist('university')
        passing_years = request.POST.getlist('passing_year')
        percentages = request.POST.getlist('percentage')

        # Create education details list
        for course_name, university, passing_year, percentage in zip(course_names, universities, passing_years, percentages):
            if all([course_name, university, passing_year, percentage]):
                education_details.append({
                    'course_name': course_name,
                    'university': university,
                    'passing_year': passing_year,
                    'percentage': percentage
                })

        # Update the education details field
        employee.education_details = education_details

        # Save employee changes
        employee.save()

        messages.success(request, 'Employee and education details updated successfully!')
        return redirect('listemp')  # Redirect to the employee list after updating

    # Fetch countries, states, and cities for the form
    countries = get_countries()
    
    # Fetch states for the employee's current country if it exists
    states = get_states(employee.country) if employee.country else []
    
    # Fetch cities for the employee's current state if it exists
    cities = get_cities(employee.state) if employee.state else []

    return render(request, 'update_emp.html', {
        'employee': employee,
        'countries': countries,
        'states': states,
        'cities': cities
    })


def check_email_exists(request):
    if request.method == 'GET':
        email = request.GET.get('email', None)
        exists = Emps.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})


def ListEmp(request):
    employees = Emps.objects.filter(deleted_status=0)  # Only show employees that are not deleted
    return render(request, 'listemp.html', {'employees': employees})

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Emps

def soft_delete_employee(request, emp_id):
    employee = get_object_or_404(Emps, id=emp_id)
    employee.deleted_status = 1  # Mark as deleted
    employee.save()
    return JsonResponse({'success': True, 'message': 'Employee deleted successfully.'})
