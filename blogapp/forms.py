# forms.py

from django import forms
from .models import BlogCategory

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name', 'required': False}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super(BlogCategoryForm, self).__init__(*args, **kwargs)
        # Explicitly set required attribute to False for both fields
        self.fields['name'].required = False
        self.fields['image'].required = False
from django import forms
from .models import Emps  # Assuming the Employee model

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Emps  # Assuming Employee model
        fields = ['full_name', 'email', 'mobile_number', 'gender', 'address', 'country', 'state', 'city', 'pincode', 
                  'course_name', 'university', 'passing_year', 'percentage']

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter your full name'
        }),
        label="Full Name"
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter your email address'
        }),
        label="Email"
    )
    
    mobile_number = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter your mobile number'
        }),
        label="Mobile Number"
    )
    
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Gender"
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-sm border',
            'rows': 3,
            'placeholder': 'Enter your address'
        }),
        label="Address"
    )
    
    country = forms.ChoiceField(
        choices=[],  # To be populated dynamically in the view
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm border',
        }),
        label="Country"
    )
    
    state = forms.ChoiceField(
        choices=[],  # To be populated dynamically in the view
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm border',
            'disabled': 'disabled',
        }),
        label="State"
    )
    
    city = forms.ChoiceField(
        choices=[],  # To be populated dynamically in the view
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm border',
            'disabled': 'disabled',
        }),
        label="City"
    )
    
    pincode = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter your pincode'
        }),
        label="Pincode"
    )

    # Education Fields (Multiple Entries)
    course_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter your course name'
        }),
        label="Course Name"
    )
    
    university = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter your university/institute/board'
        }),
        label="University/Institute/Board"
    )
    
    passing_year = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter year of passing (YYYY)'
        }),
        label="Year of Passing"
    )
    
    percentage = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm border',
            'placeholder': 'Enter percentage/class obtained'
        }),
        label="Percentage Obtained"
    )

    # Custom validation methods
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if len(pincode) != 6 or not pincode.isdigit():
            raise forms.ValidationError("Pincode must be a 6-digit number.")
        return pincode

    def clean_passing_year(self):
        passing_year = self.cleaned_data.get('passing_year')
        if len(passing_year) != 4 or not passing_year.isdigit():
            raise forms.ValidationError("Passing year must be a valid 4-digit year.")
        return passing_year
