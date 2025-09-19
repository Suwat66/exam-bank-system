from django.db import models
from accounts.models import CustomUser

class LearningArea(models.Model):
    """
    Represents a learning area, e.g., "Science and Technology", "Mathematics".
    Managed by Admins.
    """
    area_name = models.CharField(max_length=255, unique=True, verbose_name="ชื่อกลุ่มสาระการเรียนรู้")

    class Meta:
        verbose_name = "กลุ่มสาระการเรียนรู้"
        verbose_name_plural = "กลุ่มสาระการเรียนรู้"
        ordering = ['area_name']

    def __str__(self): 
        return self.area_name

class SubjectTemplate(models.Model):
    """
    Represents a subject template, e.g., "Basic Science", "Algebra".
    This is the master list of subjects, managed by Admins.
    It does not contain a course code.
    """
    subject_name = models.CharField(max_length=255, verbose_name="ชื่อรายวิชา (แม่แบบ)")
    learning_area = models.ForeignKey(LearningArea, on_delete=models.CASCADE, related_name='subject_templates', verbose_name="กลุ่มสาระการเรียนรู้")
    
    class Meta:
        unique_together = ('subject_name', 'learning_area')
        verbose_name = "แม่แบบรายวิชา"
        verbose_name_plural = "แม่แบบรายวิชา"
        ordering = ['learning_area', 'subject_name']

    def __str__(self):
        return f"{self.subject_name} ({self.learning_area.area_name})"

class GradeLevel(models.Model):
    """
    Represents a grade level, e.g., "ม.1", "ม.2".
    Managed by Admins.
    """
    grade_name = models.CharField(max_length=100, unique=True, verbose_name="ชื่อระดับชั้น")

    class Meta:
        verbose_name = "ระดับชั้น"
        verbose_name_plural = "ระดับชั้น"
        ordering = ['id']

    def __str__(self): 
        return self.grade_name

class Course(models.Model):
    """
    Represents a specific course taught by a teacher.
    This links a SubjectTemplate with a GradeLevel, a teacher-defined course code,
    and the teacher themselves.
    """
    course_code = models.CharField(max_length=20, verbose_name="รหัสวิชา")
    subject_template = models.ForeignKey(SubjectTemplate, on_delete=models.CASCADE, related_name='courses', verbose_name="รายวิชา (จากแม่แบบ)")
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, related_name='courses', verbose_name="ระดับชั้น")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses', verbose_name="ครูผู้สอน")

    class Meta:
        # Prevents the same teacher from creating the same course code twice.
        unique_together = ('course_code', 'teacher')
        verbose_name = "รายวิชาของครู"
        verbose_name_plural = "รายวิชาของครู"
        ordering = ['teacher', 'course_code']
        
    def __str__(self):
        return f"{self.course_code} - {self.subject_template.subject_name} ({self.grade_level.grade_name})"

class LearningUnit(models.Model):
    """
    Represents a learning unit within a specific Course.
    Managed by Teachers.
    """
    unit_name = models.CharField(max_length=255, verbose_name="ชื่อหน่วยการเรียนรู้")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units', verbose_name="รายวิชา")

    class Meta:
        verbose_name = "หน่วยการเรียนรู้"
        verbose_name_plural = "หน่วยการเรียนรู้"
        ordering = ['course', 'unit_name']

    def __str__(self):
        return f"{self.unit_name} ({self.course.course_code})"