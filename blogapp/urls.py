from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .import views
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path('', views.RegisterPage, name='registerpage'),
    path('register/', views.register, name='register'),
    path('loginpage',views.LoginPage,name="loginpage"),
    path('login',views.Login,name="login"),
    path('blogpage/',views.BlogPage,name="blogpage"),
    path('addblog/',views.AddBlog,name="addblog"),
    path('upload_image/upload',views.upload_image,name="upload_image"),
    path('bloglist/',views.BlogListPage,name="bloglist"),
    path('blogdetails/<int:blog_id>/', views.BlogDetailPage, name='blogdetails'),  # Include blog_id in the path
    path('deleteblog/<int:blog_id>/', views.DeleteBlog, name="deleteblog"),  # Delete blog
    path('editblog/<int:blog_id>/', views.EditBlog, name='editblog'),
    path('forgotpage/', views.ForgotPage, name='forgotpage'),
    path("verify_otp/",views.verify_otp,name="verify_otp"),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('logout/', views.LogOut, name='logout'),
    path('resetpassword/', views.ResetPassword, name='resetpassword'),


    path('addcatogiry/', views.AddBlogCategory, name='addcatogiry'),
    path('catogirylist/', views.Catogiry_List, name='catogirylist'),
    path('check_category_exists/', views.Check_category_exists, name='check_category_exists'),
    path('update_category/<int:pk>/', views.UpdateBlogCategory, name='update_category'),
    path('delete_category/', views.delete_category, name='delete_category'),
    path('fetch-categories/', views.fetch_categories, name='fetch_categories'),
    path('category_exists/', views.category_exists, name='category_exists'),

    path('check_category_in_blog/', views.check_category_in_blog, name='check_category_in_blog'),

####3#### employee ####
    path('addemp/', views.AddEmp, name='addemp'),
    path('load-states/', views.load_states, name='load-states'),
    path('load-cities/', views.load_cities, name='load-cities'),
    path('listemp/', views.ListEmp, name='listemp'),

    path('check_email/', views.check_email_exists, name='check_email'),
    path('update_emp/<int:employee_id>/', views.UpdateEmp, name='update_emp'),
    path('soft_delete_employee/<int:emp_id>/', views.soft_delete_employee, name='soft_delete_employee'),





]


if settings.DEBUG:
      urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)