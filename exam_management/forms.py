from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

from .models import Question, Choice, Exam
from core.models import Course, LearningUnit

# ==============================================================================
# Forms for Teacher's Own Data (Course, LearningUnit)
# ==============================================================================

class CourseForm(forms.ModelForm):
    """
    Form for Teachers to create and update their own courses.
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
    Form for Teachers to create and update their own learning units.
    The 'course' field's queryset is dynamically filtered in the view.
    """
    class Meta:
        model = LearningUnit
        fields = ['unit_name', 'course']
        labels = {
            'unit_name': 'ชื่อหน่วยการเรียนรู้',
            'course': 'รายวิชา',
        }
        widgets = {
            'unit_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'course': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        """
        Filters the 'course' queryset to only show courses
        belonging to the current logged-in teacher.
        """
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)


# ==============================================================================
# Forms for Question and Exam Management
# ==============================================================================

class QuestionForm(forms.ModelForm):
    """
    Form for creating and updating a Question.
    """
    class Meta:
        model = Question
        fields = [
            'question_text', 'question_type', 'bloom_level',
            'difficulty_level', 'learning_unit', 'explanation', 'image'
        ]
        labels = {
            'question_text': "เนื้อหาคำถาม",
            'question_type': "ประเภทคำถาม",
            'bloom_level': "ระดับการเรียนรู้ (Bloom's Taxonomy)",
            'difficulty_level': "ค่าความยาก (p)",
            'learning_unit': "หน่วยการเรียนรู้",
            'explanation': "คำอธิบายเฉลย",
            'image': "รูปภาพประกอบ (ถ้ามี)",
        }
        help_texts = {
            'difficulty_level': """
            <div class="text-xs text-gray-500 mt-1 space-y-1">
                <p>• <strong>ง่าย (Easy):</strong> p ≥ 0.70</p>
                <p>• <strong>ปานกลาง (Moderate):</strong> 0.30 ≤ p < 0.70</p>
                <p>• <strong>ยาก (Difficult):</strong> p < 0.30</p>
            </div>
            """,
        }
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'question_type': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'bloom_level': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'learning_unit': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'explanation': forms.Textarea(attrs={'rows': 2, 'class': 'w-full p-2 border border-gray-300 rounded-md', 'placeholder': 'คำอธิบายเพิ่มเติม (ถ้ามี)'}),
            'difficulty_level': forms.NumberInput(attrs={'step': '0.01','min': '0.0','max': '1.0','class': 'w-full p-2 border rounded-md'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }

    def __init__(self, user, *args, **kwargs):
        """
        Filters the 'learning_unit' queryset to only show units
        belonging to the current teacher's courses.
        """
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['learning_unit'].queryset = LearningUnit.objects.filter(course__teacher=user)

class BaseChoiceFormSet(forms.BaseInlineFormSet):
    """
    Custom BaseInlineFormSet for Choices to add validation logic.
    """
    def clean(self):
        super().clean()
        # self.instance is the question object
        if hasattr(self, 'instance') and self.instance and self.instance.question_type != 'MCQ':
            return

        active_forms_count = 0
        correct_choices_count = 0
        for form in self.forms:
            if hasattr(form, 'cleaned_data') and form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                active_forms_count += 1
                if form.cleaned_data.get('is_correct'):
                    correct_choices_count += 1
        
        if active_forms_count > 0 and correct_choices_count == 0:
            raise ValidationError('โปรดเลือกคำตอบที่ถูกต้องอย่างน้อย 1 ข้อ')
        
        if correct_choices_count > 1:
            raise ValidationError('สามารถเลือกคำตอบที่ถูกต้องได้เพียงข้อเดียวเท่านั้น')


ChoiceFormSet = inlineformset_factory(
    Question, 
    Choice,
    formset=BaseChoiceFormSet,
    fields=('choice_text', 'is_correct'),
    extra=4,
    can_delete=True,
    validate_min=False,
    widgets={
        'choice_text': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'เนื้อหาตัวเลือก'}),
        'is_correct': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'}),
    }
)


class ExamForm(forms.ModelForm):
    """
    Form for creating/updating an Exam.
    """
    class Meta:
        model = Exam
        fields = ['exam_name', 'course']
        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'course': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)


class AutoGenerateExamForm(forms.Form):
    """
    Form for automatically generating an exam.
    """
    exam_name = forms.CharField(label="1. ตั้งชื่อชุดข้อสอบ", max_length=255, widget=forms.TextInput(attrs={'placeholder': 'เช่น แบบทดสอบกลางภาค'}))
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), # Set to .all() initially, will be filtered in __init__
        label="2. เลือกรายวิชาของคุณ",
        empty_label="-- กรุณาเลือกรายวิชา --",
        widget=forms.Select(attrs={'id': 'id_course'})
    )
    
    learning_units = forms.ModelMultipleChoiceField(
        queryset=LearningUnit.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    num_easy = forms.IntegerField(label="ข้อง่าย (p ≥ 0.70)", min_value=0, initial=0)
    num_medium = forms.IntegerField(label="ข้อปานกลาง (0.30 ≤ p < 0.70)", min_value=0, initial=0)
    num_hard = forms.IntegerField(label="ข้อยาก (p < 0.30)", min_value=0, initial=0)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter the course queryset based on the logged-in user
        if user and user.is_authenticated:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)
        else:
            self.fields['course'].queryset = Course.objects.none()

        # If form is bound with data (e.g., on POST or validation error),
        # populate the learning_units queryset so validation can find the choices.
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['learning_units'].queryset = LearningUnit.objects.filter(course_id=course_id)
            except (ValueError, TypeError):
                # Handle cases where course_id is invalid or not present
                pass

        # Apply common styling to all relevant fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Select)):
                field.widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-md'})
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded-md text-center'})