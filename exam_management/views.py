import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # <-- ตรวจสอบ import
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import inlineformset_factory
from django import forms

from .models import Exam, Question, Choice
from core.models import Course, LearningUnit
from .forms import (
    AutoGenerateExamForm, QuestionForm, ChoiceFormSet, ExamForm,
    CourseForm, LearningUnitForm, BaseChoiceFormSet
)
from .utils import generate_pdf_exam, generate_word_exam
from .filters import QuestionFilter

# ==============================================================================
# Mixins & Decorators for Authorization
# ==============================================================================

class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin for Class-Based Views to ensure the user is an authenticated and approved teacher.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'TEACHER' and self.request.user.is_approved

    def handle_no_permission(self):
        messages.error(self.request, 'คุณต้องเข้าสู่ระบบในฐานะครูที่ได้รับอนุมัติเพื่อเข้าถึงหน้านี้')
        return redirect('accounts:login')

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin for Class-Based Views to ensure the user is an authenticated Admin.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

    def handle_no_permission(self):
        messages.error(self.request, 'คุณต้องเข้าสู่ระบบในฐานะผู้ดูแลระบบเพื่อเข้าถึงหน้านี้')
        return redirect('accounts:login')

def teacher_required(function):
    """
    Decorator for Function-Based Views to ensure the user is an authenticated and approved teacher.
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'TEACHER' and request.user.is_approved:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'คุณต้องเข้าสู่ระบบในฐานะครูที่ได้รับอนุมัติเพื่อเข้าถึงหน้านี้')
            return redirect('accounts:login')
    return wrap

# ==============================================================================
# Teacher Dashboard
# ==============================================================================

@teacher_required
def teacher_dashboard(request):
    exams = Exam.objects.filter(created_by=request.user).order_by('-created_at')
    question_count = Question.objects.filter(created_by=request.user).count()
    course_count = Course.objects.filter(teacher=request.user).count()
    context = {
        'exams': exams,
        'question_count': question_count,
        'course_count': course_count,
    }
    return render(request, 'teacher/dashboard.html', context)


# ==============================================================================
# Course Management (CRUD) Views for Teachers
# ==============================================================================

class CourseListView(TeacherRequiredMixin, ListView):
    model = Course
    template_name = 'teacher/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user).select_related('subject_template', 'grade_level').order_by('course_code')

class CourseCreateView(TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'teacher/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'เพิ่มรายวิชาใหม่สำเร็จ')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มรายวิชาของฉัน'
        return context

class CourseUpdateView(TeacherRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'teacher/course_form.html'
    success_url = reverse_lazy('course_list')

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'แก้ไขรายวิชาสำเร็จ')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'แก้ไขรายวิชาของฉัน'
        return context

class CourseDeleteView(TeacherRequiredMixin, DeleteView):
    model = Course
    template_name = 'teacher/confirm_delete_base.html'
    success_url = reverse_lazy('course_list')
    
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'ลบรายวิชา "{self.object}" สำเร็จ')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ยืนยันการลบรายวิชา'
        context['object_name'] = self.object
        context['cancel_url'] = self.success_url
        return context


# ==============================================================================
# Learning Unit Management (CRUD) Views for Teachers
# ==============================================================================

class LearningUnitListView(TeacherRequiredMixin, ListView):
    model = LearningUnit
    template_name = 'teacher/learningunit_list.html'
    context_object_name = 'units'
    paginate_by = 10

    def get_queryset(self):
        return LearningUnit.objects.filter(course__teacher=self.request.user).select_related('course', 'course__subject_template').order_by('course__course_code', 'unit_name')

class LearningUnitCreateView(TeacherRequiredMixin, CreateView):
    model = LearningUnit
    template_name = 'teacher/learningunit_form.html'
    form_class = LearningUnitForm
    success_url = reverse_lazy('learning_unit_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'เพิ่มหน่วยการเรียนรู้ใหม่สำเร็จ')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'เพิ่มหน่วยการเรียนรู้ใหม่'
        return context

class LearningUnitUpdateView(TeacherRequiredMixin, UpdateView):
    model = LearningUnit
    form_class = LearningUnitForm
    template_name = 'teacher/learningunit_form.html'
    success_url = reverse_lazy('learning_unit_list')

    def get_queryset(self):
        return LearningUnit.objects.filter(course__teacher=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'แก้ไขหน่วยการเรียนรู้สำเร็จ')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'แก้ไขหน่วยการเรียนรู้'
        return context

class LearningUnitDeleteView(TeacherRequiredMixin, DeleteView):
    model = LearningUnit
    template_name = 'teacher/confirm_delete_base.html'
    success_url = reverse_lazy('learning_unit_list')
    
    def get_queryset(self):
        return LearningUnit.objects.filter(course__teacher=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, f'ลบหน่วยการเรียนรู้ "{self.object.unit_name}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ยืนยันการลบหน่วยการเรียนรู้'
        context['object_name'] = self.object
        context['cancel_url'] = self.success_url
        return context

# ==============================================================================
# Question Management (CRUD) Views
# ==============================================================================

@teacher_required
def question_list(request):
    base_queryset = Question.objects.filter(created_by=request.user).select_related(
        'learning_unit', 'learning_unit__course__subject_template'
    ).order_by('-created_at')
    question_filter = QuestionFilter(request.GET, queryset=base_queryset, user=request.user)
    context = {
        'filter': question_filter,
        'questions': question_filter.qs,
    }
    return render(request, 'teacher/question_list.html', context)

@teacher_required
def question_manage_view(request, pk=None):
    if pk:
        question = get_object_or_404(Question, pk=pk, created_by=request.user)
        form_title = 'แก้ไขคำถาม'
        ChoiceFormSetDynamic = inlineformset_factory(
            Question, Choice, formset=BaseChoiceFormSet, 
            fields=('choice_text', 'is_correct'), extra=1,
            can_delete=True, validate_min=False, widgets={
                'choice_text': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'เนื้อหาตัวเลือก'}),
                'is_correct': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'}),
            }
        )
    else:
        question = Question()
        form_title = 'สร้างคำถามใหม่'
        ChoiceFormSetDynamic = ChoiceFormSet

    if request.method == 'POST':
        form = QuestionForm(user=request.user, data=request.POST, files=request.FILES, instance=question)
        formset = ChoiceFormSetDynamic(request.POST, instance=question)
        
        if form.is_valid():
            saved_question = form.save(commit=False)
            
            formset_is_valid = True
            if saved_question.question_type == 'MCQ':
                formset_is_valid = formset.is_valid()

            if formset_is_valid:
                saved_question.created_by = request.user
                saved_question.save()

                if saved_question.question_type == 'MCQ':
                    formset.save()
                else:
                    Choice.objects.filter(question=saved_question).delete()

                messages.success(request, f'บันทึกคำถาม "{saved_question}" สำเร็จ')
                return redirect('question_list')
    else:
        form = QuestionForm(user=request.user, instance=question)
        formset = ChoiceFormSetDynamic(instance=question)

    context = {
        'form': form,
        'formset': formset,
        'form_title': form_title,
    }
    return render(request, 'teacher/question_form.html', context)

@teacher_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk, created_by=request.user)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'ลบคำถามสำเร็จ')
        return redirect('question_list')
    context = {
        'object': question,
        'title': 'ยืนยันการลบคำถาม',
        'cancel_url': reverse_lazy('question_list')
    }
    return render(request, 'teacher/confirm_delete_base.html', context)


# ==============================================================================
# Exam Management Views
# ==============================================================================

@teacher_required
def create_exam_auto(request):
    if request.method == 'POST':
        form = AutoGenerateExamForm(user=request.user, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            course = data['course']
            
            selected_unit_ids = request.POST.getlist('learning_units')
            error_found = False
            if not selected_unit_ids:
                form.add_error('learning_units', 'คุณต้องเลือกอย่างน้อย 1 หน่วยการเรียนรู้')
                error_found = True
            
            total_questions_requested = data['num_easy'] + data['num_medium'] + data['num_hard']
            if total_questions_requested <= 0:
                form.add_error(None, 'คุณต้องกำหนดจำนวนข้อสอบอย่างน้อย 1 ข้อ')
                error_found = True
            
            if error_found:
                return render(request, 'teacher/exam_auto_form.html', {'form': form})

            base_query = Question.objects.filter(
                learning_unit_id__in=selected_unit_ids,
                created_by=request.user
            )
            
            easy_qs = list(base_query.filter(difficulty_level__gte=0.70))
            medium_qs = list(base_query.filter(difficulty_level__gte=0.30, difficulty_level__lt=0.70))
            hard_qs = list(base_query.filter(difficulty_level__lt=0.30))

            final_qs = []
            final_qs.extend(random.sample(easy_qs, min(len(easy_qs), data['num_easy'])))
            final_qs.extend(random.sample(medium_qs, min(len(medium_qs), data['num_medium'])))
            final_qs.extend(random.sample(hard_qs, min(len(hard_qs), data['num_hard'])))
            
            if not final_qs:
                messages.error(request, 'ไม่พบคำถามในคลังตามเงื่อนไขที่ระบุเลย')
                return render(request, 'teacher/exam_auto_form.html', {'form': form})

            if len(final_qs) < total_questions_requested:
                messages.warning(request, f'จำนวนคำถามในคลังไม่เพียงพอตามที่กำหนด ระบบได้สุ่มข้อสอบมาให้ {len(final_qs)} ข้อจากที่ขอ {total_questions_requested} ข้อ')

            exam = Exam.objects.create(
                exam_name=data['exam_name'],
                course=course,
                created_by=request.user
            )
            exam.questions.set(final_qs)
            messages.success(request, f'สร้างชุดข้อสอบ "{exam.exam_name}" สำเร็จ')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = AutoGenerateExamForm(user=request.user)
    
    return render(request, 'teacher/exam_auto_form.html', {'form': form})


@teacher_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)
    questions = exam.questions.prefetch_related('choices').all()
    choice_format = request.GET.get('format', 'thai')
    context = {
        'exam': exam,
        'questions': questions,
        'choice_format': choice_format,
    }
    return render(request, 'teacher/exam_detail.html', context)

class ExamUpdateView(TeacherRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'teacher/exam_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'แก้ไขชุดข้อสอบสำเร็จ')
        return reverse_lazy('teacher_dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'แก้ไขชุดข้อสอบ'
        return context

class ExamDeleteView(TeacherRequiredMixin, DeleteView):
    model = Exam
    template_name = 'teacher/confirm_delete_base.html'
    
    def get_success_url(self):
        messages.success(self.request, 'ลบชุดข้อสอบสำเร็จ')
        return reverse_lazy('teacher_dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ยืนยันการลบชุดข้อสอบ'
        context['object_name'] = self.object
        context['cancel_url'] = self.success_url
        return context

# ==============================================================================
# Exam Export Views
# ==============================================================================

@teacher_required
def export_exam_pdf(request, pk):
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)
    choice_format = request.GET.get('format', 'thai')
    pdf_buffer = generate_pdf_exam(exam, choice_format)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{exam.exam_name}.pdf"'
    return response

@teacher_required
def export_exam_word(request, pk):
    exam = get_object_or_404(Exam, pk=pk, created_by=request.user)
    choice_format = request.GET.get('format', 'thai')
    doc_buffer = generate_word_exam(exam, choice_format)
    
    response = HttpResponse(doc_buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{exam.exam_name}.docx"'
    return response

# ==============================================================================
# Admin Overview Views
# ==============================================================================

class AdminQuestionListView(AdminRequiredMixin, ListView):
    model = Question
    template_name = 'admin/question_list_overview.html'
    context_object_name = 'questions'
    paginate_by = 20
    
    def get_queryset(self):
        # Admin can view all questions in the system
        return Question.objects.select_related(
            'created_by', 
            'learning_unit__course__teacher'
        ).all().order_by('-created_at')

# --- แก้ไขจาก TeacherRequiredMixin เป็น AdminRequiredMixin ---
class AdminExamListView(AdminRequiredMixin, ListView):
    model = Exam
    template_name = 'admin/exam_list_overview.html'
    context_object_name = 'exams'
    paginate_by = 20
    
    def get_queryset(self):
        # Admin can view all exams in the system
        return Exam.objects.select_related(
            'created_by', 
            'course__teacher'
        ).all().order_by('-created_at')