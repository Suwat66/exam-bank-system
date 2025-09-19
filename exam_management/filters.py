import django_filters
from django import forms
from django.db.models import Q
from .models import Question
from core.models import LearningArea, SubjectTemplate, GradeLevel, Course, LearningUnit

class TailwindSelect(forms.Select):
    """A custom Select widget that applies default Tailwind CSS classes."""
    def __init__(self, attrs=None, choices=()):
        default_attrs = {
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-sm'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)

class QuestionFilter(django_filters.FilterSet):
    """FilterSet for the Question model."""
    course_search = django_filters.CharFilter(
        method='filter_by_course_search',
        label='ค้นหาด้วยชื่อหรือรหัสวิชา',
        widget=forms.TextInput(attrs={
            'placeholder': 'เช่น วิทยาศาสตร์ หรือ ว21101',
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm'
        })
    )
    learning_area = django_filters.ModelChoiceFilter(
        field_name='learning_unit__course__subject_template__learning_area',
        queryset=LearningArea.objects.all(),
        label='กลุ่มสาระฯ',
        widget=TailwindSelect,
        empty_label="-- ทุกกลุ่มสาระฯ --"
    )
    subject_template = django_filters.ModelChoiceFilter(
        field_name='learning_unit__course__subject_template',
        queryset=SubjectTemplate.objects.all(),
        label='รายวิชา (แม่แบบ)',
        widget=TailwindSelect,
        empty_label="-- ทุกรายวิชา --"
    )
    grade_level = django_filters.ModelChoiceFilter(
        field_name='learning_unit__course__grade_level',
        queryset=GradeLevel.objects.all(),
        label='ระดับชั้น',
        widget=TailwindSelect,
        empty_label="-- ทุกระดับชั้น --"
    )
    learning_unit = django_filters.ModelChoiceFilter(
        queryset=LearningUnit.objects.all(),
        label='หน่วยการเรียนรู้',
        widget=TailwindSelect,
        empty_label="-- ทุกหน่วยฯ --"
    )
    difficulty = django_filters.ChoiceFilter(
        label='ระดับความยาก',
        choices=(('', '-- ทั้งหมด --'), ('EASY', 'ง่าย'), ('MEDIUM', 'ปานกลาง'), ('HARD', 'ยาก')),
        method='filter_by_difficulty_category',
        widget=TailwindSelect
    )

    class Meta:
        model = Question
        fields = [] 

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            user_courses = Course.objects.filter(teacher=user)
            if user_courses.exists():
                self.form.fields['learning_unit'].queryset = LearningUnit.objects.filter(course__in=user_courses)
                
                # Filter choices based on the courses the teacher has created
                grade_ids = user_courses.values_list('grade_level_id', flat=True).distinct()
                self.form.fields['grade_level'].queryset = GradeLevel.objects.filter(id__in=grade_ids)

                template_ids = user_courses.values_list('subject_template_id', flat=True).distinct()
                self.form.fields['subject_template'].queryset = SubjectTemplate.objects.filter(id__in=template_ids)

                area_ids = SubjectTemplate.objects.filter(id__in=template_ids).values_list('learning_area_id', flat=True).distinct()
                self.form.fields['learning_area'].queryset = LearningArea.objects.filter(id__in=area_ids)
            else:
                # If teacher has no courses, make all dropdowns empty
                for field_name in ['learning_unit', 'grade_level', 'subject_template', 'learning_area']:
                    self.form.fields[field_name].queryset = self.form.fields[field_name].queryset.model.objects.none()

    def filter_by_course_search(self, queryset, name, value):
        if not value: return queryset
        return queryset.filter(
            Q(learning_unit__course__subject_template__subject_name__icontains=value) |
            Q(learning_unit__course__course_code__icontains=value)
        ).distinct()
    
    def filter_by_difficulty_category(self, queryset, name, value):
        if value == 'EASY': return queryset.filter(difficulty_level__gte=0.70)
        if value == 'MEDIUM': return queryset.filter(difficulty_level__gte=0.30, difficulty_level__lt=0.70)
        if value == 'HARD': return queryset.filter(difficulty_level__lt=0.30)
        return queryset