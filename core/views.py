from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from .models import LearningArea, SubjectTemplate, GradeLevel, LearningUnit, Course
from .forms import LearningAreaForm, SubjectTemplateForm, GradeLevelForm, LearningUnitForm

# ==============================================================================
# View สำหรับ Redirect และตรวจสอบสิทธิ์
# ==============================================================================

def index_view(request):
    """
    Redirects users based on their authentication status.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    else:
        return redirect('accounts:login')

@login_required
def dashboard_redirect_view(request):
    """
    Redirects authenticated users to the appropriate dashboard based on their role.
    """
    if request.user.role == 'ADMIN':
        return redirect('accounts:admin_dashboard')
    elif request.user.role == 'TEACHER' and request.user.is_approved:
        return redirect('teacher_dashboard')
    else:
        return redirect('accounts:login')

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure that the user is a logged-in Admin.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

# ==============================================================================
# Base Generic CRUD Views (เพื่อลดการเขียนโค้ดซ้ำ)
# ==============================================================================

class BaseListView(AdminRequiredMixin, ListView):
    paginate_by = 10

class BaseCreateView(AdminRequiredMixin, CreateView):
    template_name = 'admin/category/form_base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['success_url'] = self.success_url
        return context

class BaseUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'admin/category/form_base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['success_url'] = self.success_url
        return context

class BaseDeleteView(AdminRequiredMixin, DeleteView):
    template_name = 'admin/category/confirm_delete_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['success_url'] = self.success_url
        return context

# ==============================================================================
# CRUD Views สำหรับ Learning Area (กลุ่มสาระฯ)
# ==============================================================================

class LearningAreaListView(BaseListView):
    model = LearningArea
    template_name = 'admin/category/area_list.html'
    context_object_name = 'areas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'กลุ่มสาระการเรียนรู้'
        context['create_url'] = 'area_create'
        return context

class LearningAreaCreateView(BaseCreateView):
    model = LearningArea
    form_class = LearningAreaForm
    success_url = reverse_lazy('area_list')
    title = 'เพิ่มกลุ่มสาระฯ ใหม่'

class LearningAreaUpdateView(BaseUpdateView):
    model = LearningArea
    form_class = LearningAreaForm
    success_url = reverse_lazy('area_list')
    title = 'แก้ไขกลุ่มสาระฯ'

class LearningAreaDeleteView(BaseDeleteView):
    model = LearningArea
    success_url = reverse_lazy('area_list')
    title = 'ยืนยันการลบกลุ่มสาระฯ'

# ==============================================================================
# CRUD Views สำหรับ SubjectTemplate (แม่แบบรายวิชา)
# ==============================================================================

class SubjectTemplateListView(BaseListView):
    model = SubjectTemplate
    template_name = 'admin/category/subject_template_list.html'
    context_object_name = 'subject_templates'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'แม่แบบรายวิชา'
        context['create_url'] = 'subject_template_create'
        return context

class SubjectTemplateCreateView(BaseCreateView):
    model = SubjectTemplate
    form_class = SubjectTemplateForm
    success_url = reverse_lazy('subject_template_list')
    title = 'เพิ่มแม่แบบรายวิชาใหม่'

class SubjectTemplateUpdateView(BaseUpdateView):
    model = SubjectTemplate
    form_class = SubjectTemplateForm
    success_url = reverse_lazy('subject_template_list')
    title = 'แก้ไขแม่แบบรายวิชา'

class SubjectTemplateDeleteView(BaseDeleteView):
    model = SubjectTemplate
    success_url = reverse_lazy('subject_template_list')
    title = 'ยืนยันการลบแม่แบบรายวิชา'

# ==============================================================================
# CRUD Views สำหรับ Grade Level (ระดับชั้น)
# ==============================================================================

class GradeLevelListView(BaseListView):
    model = GradeLevel
    template_name = 'admin/category/grade_level_list.html'
    context_object_name = 'grades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ระดับชั้น'
        context['create_url'] = 'grade_level_create'
        return context

class GradeLevelCreateView(BaseCreateView):
    model = GradeLevel
    form_class = GradeLevelForm
    success_url = reverse_lazy('grade_level_list')
    title = 'เพิ่มระดับชั้นใหม่'

class GradeLevelUpdateView(BaseUpdateView):
    model = GradeLevel
    form_class = GradeLevelForm
    success_url = reverse_lazy('grade_level_list')
    title = 'แก้ไขระดับชั้น'

class GradeLevelDeleteView(BaseDeleteView):
    model = GradeLevel
    success_url = reverse_lazy('grade_level_list')
    title = 'ยืนยันการลบระดับชั้น'

# ==============================================================================
# Admin Overview Views (Read-only)
# ==============================================================================

class LearningUnitListView(BaseListView):
    model = LearningUnit
    template_name = 'admin/category/learning_unit_list.html'
    context_object_name = 'units'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'หน่วยการเรียนรู้ (ทั้งหมดในระบบ)'
        return context

# Note: Create, Update, Delete for LearningUnit should be handled by Teachers.

# ==============================================================================
# API Views (สำหรับ JavaScript/AJAX)
# ==============================================================================

def get_learning_units_api(request):
    """
    API endpoint to fetch Learning Units based on a Course ID.
    Used in the "Auto Generate Exam" form.
    """
    course_id = request.GET.get('course_id')
    units = LearningUnit.objects.filter(course_id=course_id).values('id', 'unit_name')
    return JsonResponse(list(units), safe=False)