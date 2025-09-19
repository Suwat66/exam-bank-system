from django.contrib import admin
# 1. แก้ไข import ให้นำเข้าโมเดลใหม่
from .models import SurveyResponse, SurveyRating, UsageLog

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    """
    Admin view for SurveyResponse.
    Allows viewing the main survey data and includes SurveyRating as an inline.
    """
    # 2. สร้าง Inline สำหรับแสดงคะแนนรายข้อในหน้า Response
    class SurveyRatingInline(admin.TabularInline):
        model = SurveyRating
        extra = 0 # ไม่แสดงฟอร์มเปล่าสำหรับเพิ่ม
        readonly_fields = ('question_code', 'rating') # ทำให้แก้ไขไม่ได้
        can_delete = False # ไม่อนุญาตให้ลบรายข้อ

    list_display = ('school_name', 'user', 'learning_area', 'teaching_level', 'submitted_at')
    list_filter = ('learning_area', 'teaching_level', 'teaching_experience')
    search_fields = ('school_name', 'user__username')
    
    # 3. กำหนดให้ข้อมูลทั้งหมดเป็นแบบอ่านอย่างเดียว (Read-only)
    readonly_fields = ('user', 'school_name', 'learning_area', 'teaching_level', 'teaching_experience', 
                       'usage_duration', 'suggestion_likes', 'suggestion_improvements', 'suggestion_future', 
                       'submitted_at')
    
    inlines = [SurveyRatingInline] # 4. เพิ่ม Inline เข้าไป

@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    """
    Admin view for UsageLog.
    """
    list_display = ('user', 'action', 'path', 'ip_address', 'action_time')
    list_filter = ('user',)
    search_fields = ('user__username', 'path', 'ip_address')
    readonly_fields = ('user', 'action', 'path', 'ip_address', 'action_time')

# เราไม่ต้อง register SurveyRating แยกต่างหาก เพราะมันถูกจัดการผ่าน Inline แล้ว