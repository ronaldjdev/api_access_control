# Choices para ID_CHOICES
ID_CHOICES = [
    ('NN', 'No proporciona'),
    ('RC', 'Registro civil'),
    ('TI', 'Tarjeta de identidad'),
    ('CC', 'Cedula de ciudadania'),
    ('TE', 'Tarjeta de extranjeria'),
    ('CE', 'Cedula de extranjeria'),
    ('NIT', 'N° Identificacion tributaria'),
    ('PS', 'Pasaporte'),
    ('TPE', 'Tipo de documento extranjero'),
]

# Choices para GENDER
GENDER = [
    ('NN', 'No registra'),
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otros'),
]

# Choices para MARITAL_STATUS
MARITAL_STATUS = [
    ('NN', 'No registra'),
    ('S', 'Soltero'),
    ('C', 'Casado'),
    ('UL', 'Union Libre'),
]

# Choices para RH
RH = [
    ('NN', 'No registra'),
    ('O+', 'O Positivo'),
    ('O-', 'O Negativo'),
    ('A+', 'A Positivo'),
    ('A-', 'A Negativo'),
    ('B+', 'B Positivo'),
    ('B-', 'B Negativo'),
    ('AB+', 'AB Positivo'),
    ('AB-', 'AB Negativo'),
]

# Choices para JOBS
JOBS = [
    ('NN', 'No registra'),
    ('ACCOUNTANT', 'Contador'),
    ('ADMIN', 'Administrador'),
    ('ASSISTANT_COOK', 'Auxiliar de Cocina'),
    ('CHEF', 'Chef'),
    ('EVENT_MANAGER', 'Gerente de Eventos'),
    ('GARDENER', 'Jardinero'),
    ('GOLF_PRO', 'Profesional de Golf'),
    ('HOUSEKEEPING', 'Servicio de Limpieza'),
    ('HR', 'Talento Humano'),
    ('INTERN', 'Pasante'),
    ('IT_MANAGER', 'Coordinador de Sistemas'),
    ('LIFEGUARD', 'Salvavidas'),
    ('MAINTENANCE', 'Mantenimiento General'),
    ('MAINTENANCE_GOLF', 'Mantenimiento de Golf'),
    ('MAINTENANCE_POOL', 'Mantenimiento de Piscina'),
    ('MAINTENANCE_TENNIS', 'Mantenimiento de Tenis'),
    ('MEMBER_RELATIONS', 'Relaciones con Miembros'),
    ('RECEPTION', 'Recepcionista'),
    ('SECURITY', 'Seguridad'),
    ('SERVICE_ADMIN', 'Administración de Servicios'),
    ('SERVICE_COORDINATOR', 'Coordinador de Servicios'),
    ('SUBDIRECTOR', 'Subdirector'),
    ('TENNNIS_PRO', 'Profesional de Tenis'),
    ('TREASURY', 'Tesorería'),
    ('WAITER', 'Mesero'),
    ('ACCOUNTING', 'Contabilidad'),
]



# Choices para ROLES
ROLES = [
    ('EMPLOYEE', 'Empleado'),
    ('ADMIN', 'Administrador'),
    ('SUPERUSER', 'Superusuario'),
]
