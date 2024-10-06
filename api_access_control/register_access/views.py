from django.http import JsonResponse
from api_access_control.employee.models import Employee
from .models import RegisterAccess
from .utils.qr_generator import SECRET_KEY
import jwt
import datetime

def verificar_qr(request):
    qr_data = request.POST.get('qr_data')

    try:
        decoded = jwt.decode(qr_data, SECRET_KEY, algorithms=['HS256'])
        employee_id = decoded['employee_id']
        employee = Employee.objects.get(id=employee_id)

        # Determinar si es entrada o salida
        last_register = RegisterAccess.objects.filter(employee=employee).last()
        type_access = 'IN' if last_register is None or last_register.type_access == 'OUT' else 'OUT'

        # Registrar el acceso
        RegisterAccess.objects.create(employee=employee, type_access=type_access, qr_data=qr_data)

        return JsonResponse({'status': 'success', 'type_access': type_access})
    except jwt.ExpiredSignatureError:
        return JsonResponse({'status': 'error', 'message': 'QR expirado'})
    except jwt.InvalidTokenError:
        return JsonResponse({'status': 'error', 'message': 'QR inválido'})
