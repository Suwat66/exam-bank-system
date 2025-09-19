from django.contrib import admin
from .models import Question, Choice, ShortAnswer, Exam

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # --- อัปเดต list_display และ list_filter ---
    list_display = ('__str__', 'question_type', 'bloom_level', 'get_course_code')
    list_filter = ('question_type', 'bloom_level', 'learning_unit__course__subject_template')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

    @admin.display(description='รหัสวิชา', ordering='learning_unit__course__course_code')
    def get_course_code(self, obj):
        return obj.learning_unit.course.course_code

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    # --- อัปเดต list_display และ list_filter ---
    list_display = ('exam_name', 'get_course_code', 'get_grade_name', 'created_by')
    list_filter = ('course__subject_template', 'course__grade_level', 'created_by')
    search_fields = ('exam_name', 'course__course_code')
    filter_horizontal = ('questions',)

    @admin.display(description='รหัสวิชา', ordering='course__course_code')
    def get_course_code(self, obj):
        return obj.course.course_code

    @admin.display(description='ระดับชั้น', ordering='course__grade_level')
    def get_grade_name(self, obj):
        return obj.course.grade_level.grade_name

admin.site.register(ShortAnswer)