from django.urls import path
from .views import (
    index_view,
    dashboard_redirect_view,
    get_learning_units_api,
    
    LearningAreaListView, 
    LearningAreaCreateView, 
    LearningAreaUpdateView, 
    LearningAreaDeleteView,
    
    SubjectTemplateListView, 
    SubjectTemplateCreateView, 
    SubjectTemplateUpdateView, 
    SubjectTemplateDeleteView,
    
    GradeLevelListView, 
    GradeLevelCreateView, 
    GradeLevelUpdateView, 
    GradeLevelDeleteView,
    
    LearningUnitListView,
)

# หมายเหตุ: เราไม่ได้กำหนด app_name ที่นี่ เพราะ URL ส่วนใหญ่เป็นของ Admin
# ซึ่งไม่น่าจะชนกับ URL name ของแอปฯ อื่นๆ ที่เป็นฝั่ง Teacher

urlpatterns = [
    # General Redirects and API
    path('', index_view, name='home'),
    path('dashboard/', dashboard_redirect_view, name='dashboard_redirect'),
    path('api/get-learning-units/', get_learning_units_api, name='api_get_learning_units'),
    
    # --- Admin Management URLs ---
    
    # Learning Area URLs
    path('admin/areas/', LearningAreaListView.as_view(), name='area_list'),
    path('admin/areas/new/', LearningAreaCreateView.as_view(), name='area_create'),
    path('admin/areas/<int:pk>/edit/', LearningAreaUpdateView.as_view(), name='area_update'),
    path('admin/areas/<int:pk>/delete/', LearningAreaDeleteView.as_view(), name='area_delete'),
    
    # SubjectTemplate URLs
    path('admin/subject-templates/', SubjectTemplateListView.as_view(), name='subject_template_list'),
    path('admin/subject-templates/new/', SubjectTemplateCreateView.as_view(), name='subject_template_create'),
    path('admin/subject-templates/<int:pk>/edit/', SubjectTemplateUpdateView.as_view(), name='subject_template_update'),
    path('admin/subject-templates/<int:pk>/delete/', SubjectTemplateDeleteView.as_view(), name='subject_template_delete'),

    # Grade Level URLs
    path('admin/grades/', GradeLevelListView.as_view(), name='grade_level_list'),
    path('admin/grades/new/', GradeLevelCreateView.as_view(), name='grade_level_create'),
    path('admin/grades/<int:pk>/edit/', GradeLevelUpdateView.as_view(), name='grade_level_update'),
    path('admin/grades/<int:pk>/delete/', GradeLevelDeleteView.as_view(), name='grade_level_delete'),

    # Learning Unit (Admin Overview) URL
    path('admin/units/', LearningUnitListView.as_view(), name='learning_unit_list_admin'), # Changed name to avoid conflict
]