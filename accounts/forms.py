from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

from accounts.models import CustomUser

class TeacherRegistrationForm(UserCreationForm):
    """
    A custom form for teacher registration, inheriting from Django's UserCreationForm.
    This form is customized to include first_name, last_name, and email fields,
    and to add CSS classes and placeholders for better frontend integration.
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Define placeholders and classes for each field to be styled
        placeholders = {
            'username': 'ชื่อผู้ใช้ (ภาษาอังกฤษ)',
            'first_name': 'ชื่อจริง',
            'last_name': 'นามสกุล',
            'email': 'อีเมล',
        }
        
        widget_class = 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'

        # Loop through the specified fields to apply common attributes
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder
                self.fields[field_name].widget.attrs['class'] = widget_class
                self.fields[field_name].help_text = '' # Remove default help text

        # Customize password fields specifically
        self.fields['password1'].label = "รหัสผ่าน"
        self.fields['password1'].widget.attrs['placeholder'] = 'ตั้งรหัสผ่าน (อย่างน้อย 8 ตัวอักษร)'
        self.fields['password1'].widget.attrs['class'] = widget_class

        self.fields['password2'].label = "ยืนยันรหัสผ่าน"
        self.fields['password2'].widget.attrs['placeholder'] = 'ยืนยันรหัสผ่านอีกครั้ง'
        self.fields['password2'].widget.attrs['class'] = widget_class

class LoginForm(AuthenticationForm):
    """
    A custom login form that uses styled widgets for username and password fields.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500', 
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500', 
        'placeholder': 'Password'
    }))

class AdminUserUpdateForm(forms.ModelForm):
    """
    A form for administrators to edit a user's details.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'is_approved']
        labels = {
            'username': 'ชื่อผู้ใช้ (Username)',
            'first_name': 'ชื่อจริง',
            'last_name': 'นามสกุล',
            'email': 'อีเมล',
            'role': 'บทบาท',
            'is_active': 'สถานะ Active (สามารถล็อกอินได้)',
            'is_approved': 'สถานะอนุมัติ (สำหรับครู)',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'role': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            # --- เปลี่ยน Widget ---
            'is_active': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 rounded'}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 rounded'}),
        }