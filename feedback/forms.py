from django import forms
# 1. แก้ไข import ให้นำเข้าโมเดลใหม่
from .models import SurveyResponse 

# --- สร้าง Question List สำหรับใช้ในฟอร์ม ---
SURVEY_QUESTIONS = {
    "ด้านที่ 1: การออกแบบและหน้าตาของระบบ": [
        ('1.1', 'การออกแบบโดยรวมมีความสวยงาม ทันสมัย และน่าใช้งาน'),
        ('1.2', 'การเลือกใช้สี ขนาดตัวอักษร และไอคอนมีความเหมาะสม อ่านง่าย สบายตา'),
        ('1.3', 'การจัดวางองค์ประกอบต่างๆ ในแต่ละหน้ามีความเป็นระเบียบและเข้าใจง่าย'),
    ],
    "ด้านที่ 2: ความง่ายในการใช้งาน": [
        ('2.1', 'ขั้นตอนการใช้งานระบบในภาพรวมไม่ซับซ้อน สามารถเรียนรู้ได้ง่าย'),
        ('2.2', 'เมนูและปุ่มต่างๆ สื่อความหมายได้ชัดเจน ทำให้เข้าถึงฟังก์ชันที่ต้องการได้รวดเร็ว'),
        ('2.3', 'ระบบให้คำแนะนำหรือแสดงข้อความแจ้งเตือนที่เป็นประโยชน์ต่อผู้ใช้'),
    ],
    "ด้านที่ 3: ประสิทธิภาพและความน่าเชื่อถือ": [
        ('3.1', 'ระบบมีความเร็วในการตอบสนองและโหลดหน้าต่างๆ ได้รวดเร็ว'),
        ('3.2', 'ระบบทำงานได้อย่างมีเสถียรภาพ ไม่พบข้อผิดพลาดร้ายแรงระหว่างใช้งาน'),
        ('3.3', 'มีความมั่นใจในความถูกต้องของข้อมูลที่ระบบแสดงผลและประมวลผล'),
    ],
    "ด้านที่ 4: ประโยชน์และตรงตามความต้องการ": [
        ('4.1', 'ฟังก์ชันต่างๆ ของระบบ มีประโยชน์ต่อการทำงานจริง'),
        ('4.2', 'ระบบช่วยลดขั้นตอนและประหยัดเวลาในการเตรียมการสอบได้'),
        ('4.3', 'ภาพรวมของระบบสามารถตอบสนองความต้องการในการจัดการคลังข้อสอบได้เป็นอย่างดี'),
    ],
}

# 2. เปลี่ยนชื่อฟอร์ม และเปลี่ยน model ที่อ้างอิง
class FullSurveyForm(forms.ModelForm):
    # --- ส่วนที่ 1: ข้อมูลทั่วไป ---
    learning_area = forms.ChoiceField(
        label="กลุ่มสาระการเรียนรู้",
        choices=[
            ('', '-- โปรดเลือก --'), # Add a blank choice
            ('ภาษาไทย', 'ภาษาไทย'), ('คณิตศาสตร์', 'คณิตศาสตร์'), ('วิทยาศาสตร์และเทคโนโลยี', 'วิทยาศาสตร์และเทคโนโลยี'),
            ('สังคมศึกษาฯ', 'สังคมศึกษาฯ'), ('ศิลปะ', 'ศิลปะ'), ('สุขศึกษา-พลศึกษา', 'สุขศึกษา-พลศึกษา'),
            ('การงานอาชีพ', 'การงานอาชีพ'), ('ภาษาต่างประเทศ', 'ภาษาต่างประเทศ'), ('อื่นๆ', 'อื่นๆ')
        ],
        widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )
    teaching_level = forms.ChoiceField(
        label="ระดับการสอน",
        choices=[('ประถม', 'ประถม'), ('มัธยมต้น', 'มัธยมต้น'), ('มัธยมปลาย', 'มัธยมปลาย')],
        widget=forms.RadioSelect
    )
    teaching_experience = forms.ChoiceField(
        label="ประสบการณ์การสอน (ปี)",
        choices=[('0–5', 'น้อยกว่า 5 ปี'), ('6–10', '6–10 ปี'), ('11–15', '11–15 ปี'), ('16–20', '16–20 ปี'), ('21+', '21 ปีขึ้นไป')],
        widget=forms.RadioSelect
    )
    usage_duration = forms.ChoiceField(
        label="ระยะเวลาใช้งานระบบคลังข้อสอบ",
        choices=[('<10 นาที', '<10 นาที'), ('10–30 นาที', '10–30 นาที'), ('30–60 นาที', '30–60 นาที'), ('>60 นาที', '>60 นาที')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = SurveyResponse
        fields = [
            'school_name', 'learning_area', 'teaching_level', 'teaching_experience', 'usage_duration',
            'suggestion_likes', 'suggestion_improvements', 'suggestion_future'
        ]
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md', 'placeholder': 'โปรดระบุชื่อโรงเรียนของท่าน'}),
            'suggestion_likes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'suggestion_improvements': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border border-gray-300 rounded-md'}),
            'suggestion_future': forms.Textarea(attrs={'rows': 3, 'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        }
    
    # --- ส่วนที่ 2: คะแนนรายข้อ ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # สร้างฟิลด์คะแนนแบบไดนามิกจาก SURVEY_QUESTIONS
        for category, questions in SURVEY_QUESTIONS.items():
            for code, question_text in questions:
                field_name = f'rating_{code}'
                self.fields[field_name] = forms.ChoiceField(
                    label=question_text,
                    choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')],
                    widget=forms.RadioSelect,
                    required=True
                )