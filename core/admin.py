from django.contrib import admin
from .models import LearningArea, SubjectTemplate, GradeLevel, Course, LearningUnit

@admin.register(LearningArea)
class LearningAreaAdmin(admin.ModelAdmin):
    """
    Admin interface for LearningArea model.
    """
    list_display = ('area_name',)
    search_fields = ('area_name',)

@admin.register(SubjectTemplate)
class SubjectTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for SubjectTemplate model.
    Admins use this to manage the master list of subjects.
    """
    list_display = ('subject_name', 'learning_area')
    list_filter = ('learning_area',)
    search_fields = ('subject_name',)
    ordering = ('learning_area', 'subject_name')

@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    """
    Admin interface for GradeLevel model.
    """
    list_display = ('grade_name',)
    search_fields = ('grade_name',)
    ordering = ('id',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for Course model.
    This allows admins to view/manage the specific courses created by teachers.
    """
    list_display = ('course_code', 'get_subject_name', 'get_grade_name', 'teacher')
    list_filter = ('subject_template__learning_area', 'grade_level', 'teacher')
    search_fields = ('course_code', 'subject_template__subject_name', 'teacher__username')
    ordering = ('teacher', 'course_code')
    
    # Custom methods to display related fields in list_display
    @admin.display(description='ชื่อรายวิชา', ordering='subject_template__subject_name')
    def get_subject_name(self, obj):
        return obj.subject_template.subject_name

    @admin.display(description='ระดับชั้น', ordering='grade_level__grade_name')
    def get_grade_name(self, obj):
        return obj.grade_level.grade_name

@admin.register(LearningUnit)
class LearningUnitAdmin(admin.ModelAdmin):
    """
    Admin interface for LearningUnit model.
    """
    list_display = ('unit_name', 'get_course_code', 'get_teacher')
    list_filter = ('course__subject_template', 'course__grade_level', 'course__teacher')
    search_fields = ('unit_name', 'course__course_code', 'course__subject_template__subject_name')
    ordering = ('course', 'unit_name')

    # Custom methods for more readable list_display
    @admin.display(description='รหัสวิชา', ordering='course__course_code')
    def get_course_code(self, obj):
        return obj.course.course_code

    @admin.display(description='ครูผู้สอน', ordering='course__teacher')
    def get_teacher(self, obj):
        return obj.course.teacher