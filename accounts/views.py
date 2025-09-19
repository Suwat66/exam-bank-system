from django.http import Http404
from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, views as auth_views
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from datetime import timedelta

from .forms import TeacherRegistrationForm, LoginForm
from .models import CustomUser
from exam_management.models import Question, Exam

from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import CustomUser

from django.views.generic import UpdateView, DeleteView
from .forms import AdminUserUpdateForm

# ==============================================================================
# Authentication Views (Register, Login, Logout)
# ==============================================================================

class TeacherRegisterView(CreateView):
    """
    Handles the registration process for new teachers.
    New accounts are created as inactive until approved by an admin.
    """
    model = CustomUser
    form_class = TeacherRegistrationForm
    template_name = 'registration/register.html'
    
    def get_success_url(self):
        return reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # Admin must approve this account.
        user.save()
        return redirect(self.get_success_url())

class CustomLoginView(auth_views.LoginView):
    """
    Custom login view that uses our styled LoginForm.
    """
    form_class = LoginForm
    template_name = 'registration/login.html'

def logout_view(request):
    """
    Logs out the user and redirects them to the login page.
    """
    logout(request)
    return redirect('accounts:login')


# ==============================================================================
# Admin Views (User Management & Dashboard)
# ==============================================================================

def is_admin(user):
    """
    A helper function to check if a user is an authenticated admin.
    """
    return user.is_authenticated and user.role == 'ADMIN'

@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Displays the admin dashboard, including stats cards, a registration chart,
    and a list of teachers pending approval.
    """
    # --- Data for Stat Cards ---
    pending_teachers = CustomUser.objects.filter(role='TEACHER', is_approved=False, is_active=False)
    approved_teachers_count = CustomUser.objects.filter(role='TEACHER', is_approved=True).count()
    total_questions = Question.objects.count()
    total_exams = Exam.objects.count()

    # --- Query and process data for the registration chart (last 6 months) ---
    six_months_ago = now().date() - timedelta(days=180)
    
    registrations = CustomUser.objects.filter(
        role='TEACHER',
        date_joined__gte=six_months_ago
    ).annotate(
        month=TruncMonth('date_joined')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')

    # Prepare data structure for the last 6 months
    chart_data_dict = {}
    for i in range(5, -1, -1): # Loop from 5 down to 0 for correct month order
        # Calculate the date for each of the last 6 months
        month_date = (now().date().replace(day=1) - timedelta(days=i*30))
        # Use year-month as the key
        chart_data_dict[month_date.strftime("%Y-%m")] = 0

    # Populate the dictionary with actual registration counts
    for reg in registrations:
        month_str = reg['month'].strftime("%Y-%m")
        if month_str in chart_data_dict:
            chart_data_dict[month_str] = reg['count']
    
    # Convert dictionary to lists for Chart.js
    sorted_months = sorted(chart_data_dict.keys())
    
    thai_months = {
        '01': "ม.ค.", '02': "ก.พ.", '03': "มี.ค.", '04': "เม.ย.", '05': "พ.ค.", '06': "มิ.ย.",
        '07': "ก.ค.", '08': "ส.ค.", '09': "ก.ย.", '10': "ต.ค.", '11': "พ.ย.", '12': "ธ.ค."
    }
    chart_labels = [thai_months[month.split('-')[1]] for month in sorted_months]
    chart_data = [chart_data_dict[month] for month in sorted_months]
    
    context = {
        'pending_teachers': pending_teachers,
        'approved_teachers_count': approved_teachers_count,
        'total_questions': total_questions,
        'total_exams': total_exams,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin)
def approve_teacher(request, user_id):
    """
    Approves a teacher's account, making it active and usable.
    """
    try:
        teacher = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        raise Http404("ไม่พบผู้ใช้งานตาม ID ที่ระบุ")

    teacher.role = CustomUser.Role.TEACHER
    teacher.is_active = True
    teacher.is_approved = True
    teacher.save()
    
    # --- 2. แก้ไขการเรียกใช้ messages ---
    messages.success(request, f'อนุมัติบัญชี "{teacher.username}" เรียบร้อยแล้ว')
    
    return redirect('accounts:admin_dashboard')

@user_passes_test(is_admin)
def reject_teacher(request, user_id):
    """
    Rejects a teacher's registration request by deleting the account.
    """
    try:
        teacher = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        raise Http404("ไม่พบผู้ใช้งานตาม ID ที่ระบุ")
        
    username = teacher.username
    teacher.delete()
    
    # --- 3. (Good Practice) เพิ่ม message ที่นี่ด้วย ---
    messages.success(request, f'ปฏิเสธและลบบัญชี "{username}" เรียบร้อยแล้ว')
    
    return redirect('accounts:admin_dashboard')

class AdminUserListView(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')

# ==============================================================================
# Admin CRUD for Users
# ==============================================================================

class AdminUserUpdateView(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = AdminUserUpdateForm
    template_name = 'admin/user_form.html'
    success_url = reverse_lazy('accounts:admin_user_list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

    def form_valid(self, form):
        messages.success(self.request, f'อัปเดตข้อมูลผู้ใช้ "{form.instance.username}" เรียบร้อยแล้ว')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขข้อมูลผู้ใช้: {self.object.username}'
        return context

class AdminUserDeleteView(UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'admin/confirm_delete_user.html' # ใช้ template เฉพาะ
    success_url = reverse_lazy('accounts:admin_user_list')
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'ADMIN'

    def form_valid(self, form):
        # ป้องกันไม่ให้ Admin ลบตัวเอง
        if self.object == self.request.user:
            messages.error(self.request, 'ไม่สามารถลบบัญชีของตัวเองได้')
            return redirect(self.success_url)
            
        messages.success(self.request, f'ลบบัญชีผู้ใช้ "{self.object.username}" เรียบร้อยแล้ว')
        return super().form_valid(form)