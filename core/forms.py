from django import forms
from .models import LearningArea, SubjectTemplate, GradeLevel, Course, LearningUnit

# ==============================================================================
# Forms for Admin Management
# ==============================================================================

class LearningAreaForm(forms.ModelForm):
    """
    Form for Admin to create and update LearningArea.
    """
    class Meta:
        model = LearningArea
        fields = ['area_name']
        labels = {
            'area_name': 'ชื่อกลุ่มสาระการเรียนรู้',
        }
        widgets = {
            'area_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }

class SubjectTemplateForm(forms.ModelForm):
    class Meta:
        model = SubjectTemplate
        fields = ['subject_name', 'learning_area']
        labels = {
            'subject_name': 'ชื่อรายวิชา (แม่แบบ)',
            'learning_area': 'กลุ่มสาระการเรียนรู้',
        }
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'learning_area': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }

class GradeLevelForm(forms.ModelForm):
    """
    Form for Admin to create and update GradeLevel.
    """
    class Meta:
        model = GradeLevel
        fields = ['grade_name']
        labels = {
            'grade_name': 'ชื่อระดับชั้น',
        }
        widgets = {
            'grade_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }

# Note: The following forms (CourseForm, LearningUnitForm) are managed by Teachers.
# They are often placed in the app where the primary interaction occurs
# (e.g., 'exam_management/forms.py'). However, keeping them here is also a valid
# organizational choice if 'core' is treated as a central hub for all core object forms.

class CourseForm(forms.ModelForm):
    """
    Form for Teachers to create and update their own Courses.
    """
    class Meta:
        model = Course
        fields = ['course_code', 'subject_template', 'grade_level']
        labels = {
            'course_code': 'รหัสวิชา',
            'subject_template': 'รายวิชา (จากแม่แบบ)',
            'grade_level': 'ระดับชั้น',
        }
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'subject_template': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'grade_level': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }

class LearningUnitForm(forms.ModelForm):
    """
    Form for Teachers to create and update their own Learning Units.
    """
    class Meta:
        model = LearningUnit
        fields = ['unit_name', 'course']
        labels = {
            'unit_name': 'ชื่อหน่วยการเรียนรู้',
            'course': 'รายวิชา (ของฉัน)',
        }
        widgets = {
            'unit_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'course': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }

    def __init__(self, user, *args, **kwargs):
        """
        Filter the 'course' queryset to only show courses
        belonging to the current logged-in teacher.
        """
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)