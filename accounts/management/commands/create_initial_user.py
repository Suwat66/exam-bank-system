import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# ใช้ get_user_model() เพื่อให้ทำงานกับ CustomUser ของเราได้
CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Creates an initial superuser from environment variables for Render deployment'

    def handle(self, *args, **kwargs):
        # 1. ดึงข้อมูลจาก Environment Variables
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        # 2. ตรวจสอบว่ามีการตั้งค่าครบถ้วนหรือไม่
        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR(
                'Please set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD environment variables.'
            ))
            return

        # 3. ตรวจสอบว่ามีผู้ใช้นี้อยู่แล้วหรือยัง
        if not CustomUser.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Creating superuser: {username}'))
            
            # 4. สร้าง Superuser พร้อมตั้งค่า Role และสถานะ
            CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='ADMIN',
                is_approved=True
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists. Skipping creation.'))