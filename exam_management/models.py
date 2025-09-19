from django.db import models
from accounts.models import CustomUser
from core.models import Course, LearningUnit # Updated import

class Question(models.Model):
    """
    Represents a single question in the question bank.
    This model is now indirectly linked to Course via LearningUnit.
    """
    class QuestionType(models.TextChoices):
        MCQ = 'MCQ', 'ประเภทปรนัย (Multiple Choice)'
        SHORT = 'SHORT', 'ประเภทอัตนัยสั้น (Short Answer)'

    class BloomLevel(models.TextChoices):
        REMEMBER = 'REMEMBER', 'ความรู้ความจำ (Remembering)'
        UNDERSTAND = 'UNDERSTAND', 'ความเข้าใจ (Understanding)'
        APPLY = 'APPLY', 'การนำไปใช้ (Applying)'
        ANALYZE = 'ANALYZE', 'การวิเคราะห์ (Analyzing)'
        EVALUATE = 'EVALUATE', 'การประเมินค่า (Evaluating)'
        CREATE = 'CREATE', 'การสร้างสรรค์ (Creating)'

    question_text = models.TextField()
    question_type = models.CharField(
        max_length=10, 
        choices=QuestionType.choices
    )
    difficulty_level = models.FloatField(
        default=0.5,
        help_text="ค่าดัชนีความยาก (p-value) ระหว่าง 0.00 ถึง 1.00"
    )
    bloom_level = models.CharField(
        max_length=20,
        choices=BloomLevel.choices,
        default=BloomLevel.UNDERSTAND,
        verbose_name="ระดับการเรียนรู้ (Bloom)"
    )
    image = models.ImageField(
        upload_to='question_images/', # <-- ไฟล์จะถูกเก็บใน media/question_images/
        blank=True, 
        null=True,
        verbose_name="รูปภาพประกอบ"
    )
    explanation = models.TextField(blank=True, null=True)
    learning_unit = models.ForeignKey(
        LearningUnit, 
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_difficulty_category(self):
        try:
            p_value = float(self.difficulty_level)
        except (ValueError, TypeError):
            return "N/A"
        if p_value >= 0.70: return 'ง่าย (Easy)'
        elif p_value >= 0.30: return 'ปานกลาง (Moderate)'
        else: return 'ยาก (Difficult)'

    @property
    def get_difficulty_category_tag(self):
        try:
            p_value = float(self.difficulty_level)
        except (ValueError, TypeError):
            return "UNKNOWN"
        if p_value >= 0.70: return 'EASY'
        elif p_value >= 0.30: return 'MEDIUM'
        else: return 'HARD'

    def __str__(self):
        return self.question_text[:50] + '...'

class Choice(models.Model):
    """
    Represents a single choice for a Multiple Choice Question (MCQ).
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class ShortAnswer(models.Model):
    """
    Represents the correct answer for a Short Answer question.
    """
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='short_answer')
    answer_text = models.CharField(max_length=500)
    
    def __str__(self):
        return self.answer_text

class Exam(models.Model):
    """
    Represents a set of questions compiled into an exam.
    This model now directly links to a Course, which defines the
    subject, grade, and course code.
    """
    exam_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="รายวิชา")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(Question, related_name='exams')

    def __str__(self):
        return f"{self.exam_name} ({self.course.course_code})"