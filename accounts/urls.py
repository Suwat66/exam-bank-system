from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    AdminUserListView, TeacherRegisterView, CustomLoginView, logout_view,
    admin_dashboard, approve_teacher, reject_teacher, AdminUserListView, AdminUserListView, AdminUserUpdateView, AdminUserDeleteView
)

# กำหนด Namespace สำหรับ URL ทั้งหมดในแอปฯ นี้ เพื่อป้องกัน URL name ชนกัน
app_name = 'accounts'

urlpatterns = [
    # URLs สำหรับ User ทั่วไป (Register, Login, Logout)
    path('register/', TeacherRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    
    # URLs สำหรับ Admin จัดการ Teacher
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/approve/<int:user_id>/', approve_teacher, name='approve_teacher'),
    path('admin/reject/<int:user_id>/', reject_teacher, name='reject_teacher'),

    # --- Password Reset URLs (ฉบับสมบูรณ์) ---
    
    # 1. หน้าขอรีเซ็ตรหัสผ่าน (กรอกอีเมล)
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url=reverse_lazy('accounts:password_reset_done')
         ), 
         name='password_reset'),
    
    # 2. หน้าแจ้งว่าส่งอีเมลสำเร็จแล้ว
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    # 3. หน้าตั้งรหัสผ่านใหม่ (หลังจากคลิกลิงก์ในอีเมล)
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')
         ), 
         name='password_reset_confirm'),
         
    # 4. หน้าแจ้งว่าตั้งรหัสผ่านใหม่สำเร็จแล้ว
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    path('admin/users/', AdminUserListView.as_view(), name='admin_user_list'),

    path('admin/users/<int:pk>/edit/', AdminUserUpdateView.as_view(), name='admin_user_update'),
    path('admin/users/<int:pk>/delete/', AdminUserDeleteView.as_view(), name='admin_user_delete'),

]