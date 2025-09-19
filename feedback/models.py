from django.db import models
from accounts.models import CustomUser

class UsageLog(models.Model):
    """
    Stores a log of user activities throughout the system.
    This is populated by the UsageLogMiddleware.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    action_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{user_info} performed '{self.action}' at {self.action_time.strftime('%Y-%m-%d %H:%M')}"

# --- สร้าง Model ใหม่ 2 ตัว ---
class SurveyResponse(models.Model):
    """
    เก็บข้อมูลทั่วไปและข้อเสนอแนะของผู้ตอบแบบสอบถามแต่ละคน
    """
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    school_name = models.CharField(max_length=255, verbose_name="สังกัด/โรงเรียน")
    learning_area = models.CharField(max_length=100, verbose_name="กลุ่มสาระการเรียนรู้")
    teaching_level = models.CharField(max_length=50, verbose_name="ระดับการสอน")
    teaching_experience = models.CharField(max_length=20, verbose_name="ประสบการณ์การสอน (ปี)")
    usage_duration = models.CharField(max_length=20, verbose_name="ระยะเวลาใช้งานระบบ")
    
    suggestion_likes = models.TextField(blank=True, null=True, verbose_name="สิ่งที่ชื่นชอบมากที่สุด")
    suggestion_improvements = models.TextField(blank=True, null=True, verbose_name="สิ่งที่ต้องการให้ปรับปรุง")
    suggestion_future = models.TextField(blank=True, null=True, verbose_name="ข้อเสนอแนะอื่นๆ")
    
    is_locked = models.BooleanField(default=True, verbose_name="สถานะการล็อก")
    
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response from {self.school_name} on {self.submitted_at.strftime('%Y-%m-%d')}"

class SurveyRating(models.Model):
    """
    เก็บคะแนนรายข้อของแบบสอบถามแต่ละฉบับ
    """
    RATING_CHOICES = [(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')]
    
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='ratings')
    question_code = models.CharField(max_length=10, verbose_name="รหัสคำถามประเมิน") # เช่น '1.1', '2.3'
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="คะแนน")

    def __str__(self):
        return f"{self.response} - Q{self.question_code}: {self.rating} stars"