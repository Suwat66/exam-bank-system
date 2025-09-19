from django.urls import path
from . import views
from .views import (
    ExamUpdateView, ExamDeleteView,
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    # --- 1. Import Views ใหม่สำหรับ LearningUnit ---
    LearningUnitListView, LearningUnitCreateView, LearningUnitUpdateView, LearningUnitDeleteView,
    AdminQuestionListView, AdminExamListView
)

urlpatterns = [
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # Course Management URLs
    path('teacher/courses/', CourseListView.as_view(), name='course_list'),
    path('teacher/courses/new/', CourseCreateView.as_view(), name='course_create'),
    path('teacher/courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_update'),
    path('teacher/courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # --- 2. เพิ่ม URLs ใหม่สำหรับ Learning Unit Management ---
    path('teacher/units/', LearningUnitListView.as_view(), name='learning_unit_list'),
    path('teacher/units/new/', LearningUnitCreateView.as_view(), name='learning_unit_create'),
    path('teacher/units/<int:pk>/edit/', LearningUnitUpdateView.as_view(), name='learning_unit_update'),
    path('teacher/units/<int:pk>/delete/', LearningUnitDeleteView.as_view(), name='learning_unit_delete'),

    # ... URLs ของ Exam ...
    path('exam/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exam/create/auto/', views.create_exam_auto, name='create_exam_auto'),
    path('exam/<int:pk>/edit/', ExamUpdateView.as_view(), name='exam_update'),
    path('exam/<int:pk>/delete/', ExamDeleteView.as_view(), name='exam_delete'),
    path('exam/<int:pk>/export/pdf/', views.export_exam_pdf, name='export_pdf'),
    path('exam/<int:pk>/export/word/', views.export_exam_word, name='export_word'),

    # ... URLs ของ Question ...
    path('teacher/questions/', views.question_list, name='question_list'),
    path('teacher/questions/new/', views.question_manage_view, name='question_create'),
    path('teacher/questions/<int:pk>/edit/', views.question_manage_view, name='question_update'),

    path('teacher/questions/<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('admin/questions/overview/', AdminQuestionListView.as_view(), name='admin_question_list'),
    path('admin/exams/overview/', AdminExamListView.as_view(), name='admin_exam_list'),
]