import django_filters
from django import forms
from .models import UsageLog
from accounts.models import CustomUser

class LogFilter(django_filters.FilterSet):
    """
    FilterSet สำหรับ UsageLog เพื่อให้ Admin สามารถกรองตามผู้ใช้และช่วงเวลาได้
    """
    # Filter ตาม User (Dropdown)
    user = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all(),
        label='ผู้ใช้งาน',
        widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm'})
    )
    
    # Filter ตามวันที่เริ่มต้น
    start_date = django_filters.DateFilter(
        field_name='action_time',
        lookup_expr='gte', # gte = Greater than or equal to
        label='ตั้งแต่วันที่',
        widget=forms.DateInput(attrs={
            'type': 'date', # ใช้ HTML5 date picker
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm'
        })
    )
    
    # Filter ตามวันที่สิ้นสุด
    end_date = django_filters.DateFilter(
        field_name='action_time',
        lookup_expr='lte', # lte = Less than or equal to
        label='ถึงวันที่',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm'
        })
    )

    class Meta:
        model = UsageLog
        fields = ['user', 'start_date', 'end_date']