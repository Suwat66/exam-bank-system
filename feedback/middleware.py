from .models import UsageLog

def get_client_ip(request):
    """
    ฟังก์ชันสำหรับดึง IP Address ของผู้ใช้งาน
    จะตรวจสอบจาก HTTP header หลายๆ ตัว เพื่อให้รองรับกรณีที่อยู่หลัง proxy
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class UsageLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and not request.path.startswith('/admin/'):
            action_description = f"{request.method} on {request.path}"
            
            # --- ดึง IP และเพิ่มเข้าไปตอนสร้าง Log ---
            client_ip = get_client_ip(request)
            
            UsageLog.objects.create(
                user=request.user,
                action=action_description,
                path=request.path,
                ip_address=client_ip # <-- เพิ่ม IP Address ที่นี่
            )
        
        return response