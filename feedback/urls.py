from django.urls import path
from .views import (
    survey_view, 
    usage_log_view, 
    survey_results_view, 
    export_surveys_excel, 
    clear_surveys_view,
    export_logs_excel,
    manage_survey_requests,
    unlock_survey,
    clear_logs_view
)

# กำหนด Namespace สำหรับ URL ทั้งหมดในแอปฯ นี้
app_name = 'feedback'

urlpatterns = [
    # Teacher URL
    path('feedback/survey/', survey_view, name='survey_submit'),

    # Admin URLs for Survey Management
    path('admin/surveys/', survey_results_view, name='survey_results'),
    path('admin/surveys/clear/', clear_surveys_view, name='clear_surveys'),
    path('admin/surveys/export/excel/', export_surveys_excel, name='export_surveys_excel'),
    path('admin/surveys/requests/', manage_survey_requests, name='manage_survey_requests'),
    path('admin/surveys/unlock/<int:response_id>/', unlock_survey, name='unlock_survey'),

    # Admin URLs for Usage Log Management
    path('admin/logs/', usage_log_view, name='usage_logs'),
    path('admin/logs/export/excel/', export_logs_excel, name='export_logs_excel'),
    
    path('admin/logs/clear/', clear_logs_view, name='clear_logs'),
]