import pytz
from datetime import timedelta
from math import floor, ceil
import holidays



def custom_round(value):
    """
    Redondea el valor al entero siguiente si el decimal es mayor a 0.75,
    de lo contrario, al entero anterior.
    """
    decimal_part = floor(value) + 0.75
    if value > decimal_part:
        return ceil(value)
    else:
        return floor(value)


# Función para determinar si el día es festivo o domingo
def is_sunday_or_holiday(date):
    colombian_holidays = holidays.Colombia()
    return date.weekday() == 6 or date.date() in colombian_holidays

# Función para calcular las horas trabajadas
def calculate_total_hours(entry, exit, job):
    work_duration = exit - entry
    total_hours = work_duration.total_seconds() / 3600  # Convertimos a horas

    # Ajuste según el tipo de trabajo
    if job in ["HOUSEKEEPING", "GARDENER", "MAINTENANCE"]:
        
        total_hours -= 1.5
    elif job == "GOLF_PRO":
        total_hours -= 2
    elif job == "TENNIS_PRO":
        total_hours -= 1

    return total_hours

# Función para obtener las horas extras diurnas
def calculate_day_extra_hours(user_entry, user_exit, standard_work_hours, tz=pytz.timezone('America/Bogota')):
    
    """
    Calcula las horas extras diurnas trabajadas por un usuario, es decir, las horas
    trabajadas entre las 7 AM y las 9 PM, menos las horas de trabajo estándar del día.
    """
    
    user_entry = user_entry.astimezone(tz)  # Convertir la entrada a la zona horaria local
    user_exit = user_exit.astimezone(tz) 
    day_extra_start = user_entry.replace(hour=7, minute=0, second=0, microsecond=0)
    day_extra_end = user_entry.replace(hour=20, minute=59, second=59, microsecond=999999)

    diurnal_worked = 0
    if user_exit > day_extra_start:
        diurnal_worked = (min(user_exit, day_extra_end) - max(user_entry, day_extra_start)).total_seconds() / 3600

    return max(diurnal_worked - standard_work_hours, 0)

# Función para obtener las horas extras nocturnas
def calculate_night_extra_hours(user_entry, user_exit, tz=pytz.timezone('America/Bogota')):
    """
    Calcula las horas extras nocturnas trabajadas por un usuario, es decir, las horas trabajadas 
    entre las 9:00 PM (21:00) y las 6:59 AM (06:59) del día siguiente.

    Parámetros:
    - user_entry: datetime que representa la hora de entrada del usuario (en UTC).
    - user_exit: datetime que representa la hora de salida del usuario (en UTC).
    - tz: zona horaria local (por defecto es Bogotá).

    Retorna:
    - nocturnal_worked: cantidad de horas trabajadas en el periodo nocturno (en horas).
    """
    
    # Asegurarse de que las fechas estén en la zona horaria correcta
    user_entry = user_entry.astimezone(tz)  # Convertir la entrada a la zona horaria local
    user_exit = user_exit.astimezone(tz)  # Convertir la salida a la zona horaria local

    # Mostrar las fechas convertidas para depuración
    print(f"⏰ Entrada ajustada: {user_entry}")
    print(f"⏰ Salida ajustada: {user_exit}")
    
    # Definir la hora de inicio del trabajo nocturno: 21:00 (9 PM)
    night_extra_start = user_entry.replace(hour=21, minute=0, second=0, microsecond=0)
    
    # Definir la hora de fin del trabajo nocturno: 06:59 del día siguiente (6:59 AM)
    night_extra_end = user_entry.replace(hour=6, minute=59, second=59, microsecond=999999) + timedelta(days=1)

    # Mostrar los límites de trabajo nocturno para depuración
    print(f"🕘 Rango nocturno: {night_extra_start} a {night_extra_end}")
    
    # Inicializar la variable de horas nocturnas trabajadas
    nocturnal_worked = 0
    
    # Verificar si la hora de salida es posterior a las 21:00 (inicio del trabajo nocturno)
    if user_exit > night_extra_start:
        # Calcular el periodo de superposición entre la entrada/salida y el rango nocturno
        start_overlap = max(user_entry, night_extra_start)  # Determinar la hora de inicio del solapamiento
        end_overlap = min(user_exit, night_extra_end)  # Determinar la hora de fin del solapamiento
        
        # Verificar si hay solapamiento válido entre las horas de trabajo y las horas nocturnas
        if start_overlap < end_overlap:
            # Calcular las horas nocturnas trabajadas en el solapamiento y convertirlo a horas
            nocturnal_worked = (end_overlap - start_overlap).total_seconds() / 3600
            
        # Mostrar el solapamiento y las horas nocturnas trabajadas para depuración
        print(f"🔄 Solapamiento: {start_overlap} a {end_overlap}")
        print(f"⏳ Horas trabajadas en el período nocturno: {nocturnal_worked} horas")

    # Retornar las horas nocturnas trabajadas
    return nocturnal_worked