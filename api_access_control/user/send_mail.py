from django.core.mail import send_mail
from django.conf import settings


def enviar_correos_empleados():
    empleados_prueba = [
        {
            "id_card": "16862247",
            "username": "holmesa",
            "email": "example1@example.com",
            "name": "Holmes",
            "last_name": "Achipiz Paz",
            "password": "16862247",
        },
        {
            "id_card": "76319223",
            "username": "juancarlosa",
            "email": "Juanca-alvarado@hotmail.com",
            "name": "Juan Carlos",
            "last_name": "Alvarado",
            "password": "76319223",
        },
        {
            "id_card": "10297603",
            "username": "angelwa",
            "email": "example2@example.com",
            "name": "Angel Wilder",
            "last_name": "Ante Urrea",
            "password": "10297603",
        },
        {
            "id_card": "10540456",
            "username": "danieleb",
            "email": "subdirector@clubcampestrepopayan.com",
            "name": "Daniel Enrique",
            "last_name": "Bermudez Campo",
            "password": "10540456",
        },
        {
            "id_card": "10546617",
            "username": "rodrigoc",
            "email": "example3@example.com",
            "name": "Rodrigo Gustavo",
            "last_name": "Calapsu Casallas",
            "password": "10546617",
        },
        {
            "id_card": "10585228",
            "username": "cristobalc",
            "email": "example4@example.com",
            "name": "Cristobal Andres",
            "last_name": "Ceron Quinayas",
            "password": "10585228",
        },
        {
            "id_card": "1061789331",
            "username": "ronaldec",
            "email": "eronald2009@gmail.com",
            "name": "Ronald Javier",
            "last_name": "Echeverry Caicedo",
            "password": "1061789331",
        },
        {
            "id_card": "1061784569",
            "username": "yiselag",
            "email": "yiselagiraldosuarez@gmail.com",
            "name": "Yisela",
            "last_name": "Giraldo Suarez",
            "password": "1061784569",
        },
        {
            "id_card": "1061712932",
            "username": "claudiag",
            "email": "example5@example.com",
            "name": "Claudia Liceth",
            "last_name": "Guerrero Suarez",
            "password": "1061712932",
        },
        {
            "id_card": "76313887",
            "username": "arleya",
            "email": "example6@example.com",
            "name": "Arley",
            "last_name": "Hernandez Alegria",
            "password": "76313887",
        },
        {
            "id_card": "1002971249",
            "username": "dianacm",
            "email": "manquillocarolina377@gmail.com",
            "name": "Diana Carolina",
            "last_name": "Manquillo Quira",
            "password": "1002971249",
        },
        {
            "id_card": "34567270",
            "username": "luzgm",
            "email": "Mmartinez34567270@gmail.com",
            "name": "Luz Milvia",
            "last_name": "Martinez Garcia",
            "password": "34567270",
        },
        {
            "id_card": "34331649",
            "username": "kellybm",
            "email": "example7@example.com",
            "name": "Kelly Johana",
            "last_name": "Mendez Benavidez",
            "password": "34331649",
        },
        {
            "id_card": "1061777074",
            "username": "kelinel",
            "email": "elianita948@hotmail.com",
            "name": "Kelin Eliana",
            "last_name": "Montenegro Muñoz",
            "password": "1061777074",
        },
        {
            "id_card": "1002958597",
            "username": "yerlynm",
            "email": "yerlynataliamunoz@gmail.com",
            "name": "Yerly Natalia",
            "last_name": "Muñoz Campo",
            "password": "1002958597",
        },
        {
            "id_card": "17645858",
            "username": "edgarn",
            "email": "example8@example.com",
            "name": "Edgar",
            "last_name": "Nieto Malagon",
            "password": "17645858",
        },
        {
            "id_card": "1144085432",
            "username": "danielao",
            "email": "danielaoa0418@hotmail.com",
            "name": "Daniela",
            "last_name": "Ordoñez Aracu",
            "password": "1144085432",
        },
        {
            "id_card": "1002966519",
            "username": "kevinop",
            "email": "Kebspalacios2u@gmail.com",
            "name": "Kevin Gabriel",
            "last_name": "Palacios Ortega",
            "password": "1002966519",
        },
        {
            "id_card": "10294498",
            "username": "wilsonpp",
            "email": "Wilsonpalacios57@gmail.com",
            "name": "Wilson",
            "last_name": "Palacios Paz",
            "password": "10294498",
        },
        {
            "id_card": "1003102677",
            "username": "valeriap",
            "email": "valeriaperafan15@gmail.com",
            "name": "Valeria",
            "last_name": "Perafan Carlosama",
            "password": "1003102677",
        },
        {
            "id_card": "10303108",
            "username": "edwinrf",
            "email": "Edwin.ruco@hotmail.com",
            "name": "Edwin",
            "last_name": "Ruco Fernandez",
            "password": "10303108",
        },
        {
            "id_card": "4664287",
            "username": "gabriela",
            "email": "example9@example.com",
            "name": "Gabriel Lino",
            "last_name": "Ruiz Astaiza",
            "password": "4664287",
        },
        {
            "id_card": "76305915",
            "username": "harolds",
            "email": "example10@example.com",
            "name": "Harold Hober",
            "last_name": "Saenz Gomez",
            "password": "76305915",
        },
        {
            "id_card": "4673317",
            "username": "brayanas",
            "email": "example11@example.com",
            "name": "Brayan Alexander",
            "last_name": "Salinas Ante",
            "password": "4673317",
        },
        {
            "id_card": "1061822052",
            "username": "camilas",
            "email": "alejandra-urrea@outlook.com",
            "name": "Camila Alejandra",
            "last_name": "Sarria Urrea",
            "password": "1061822052",
        },
        {
            "id_card": "1072656131",
            "username": "marias",
            "email": "director@clubcampestrepopayan.com",
            "name": "Maria Antonia",
            "last_name": "Segura Simmonds",
            "password": "1072656131",
        },
        {
            "id_card": "18125401",
            "username": "josevs",
            "email": "example12@example.com",
            "name": "Jose Leuceres",
            "last_name": "Sierra Veles",
            "password": "18125401",
        },
        {
            "id_card": "1058546147",
            "username": "camiloa",
            "email": "camilogalindezz2112@gmail.com",
            "name": "Camilo Andres",
            "last_name": "Suarez Galindez",
            "password": "1058546147",
        },
        {
            "id_card": "25279146",
            "username": "ceneidato",
            "email": "example13@example.com",
            "name": "Ceneida",
            "last_name": "Tunubala Ordoñez",
            "password": "25279146",
        },
        {
            "id_card": "25594389",
            "username": "cieloum",
            "email": "example14@example.com",
            "name": "Cielo Beany",
            "last_name": "Urbano Miranda",
            "password": "25594389",
        },
        {
            "id_card": "10547004",
            "username": "edgarv",
            "email": "example15@example.com",
            "name": "Edgar Jose",
            "last_name": "Valencia Medina",
            "password": "10547004",
        },
        {
            "id_card": "10540615",
            "username": "luisv",
            "email": "example16@example.com",
            "name": "Luis Guillermo",
            "last_name": "Vasquez Torres",
            "password": "10540615",
        },
        {
            "id_card": "1061771121",
            "username": "jhonyv",
            "email": "jhonytrlchef@gmail.com",
            "name": "Jhony Anyelo",
            "last_name": "Velasco Chaves",
            "password": "1061771121",
        },
    ]
    for empleado in empleados_prueba:
        # Construye el link de inicio de sesión, ajusta la URL según tu proyecto
        # Cambia 'login' al nombre de la ruta del login
        full_login_url = "https://nikaac.vercel.app/auth/sign-in"  # Cambia a la URL real de tu proyecto

        # Mensaje y asunto del correo
        subject = "Información de acceso a la plataforma"
        message = f"""
        Hola {empleado['name']} {empleado['last_name']},

        Bienvenido a la plataforma de Nika: Access Control!
        Con esto damos inicio al plan piloto de Nika: Access Control
        una plataforma de control de acceso y registro de empleados.

        Estos son tus datos de acceso:        

        Tu ID de usuario es: {empleado['id_card']}
        Tu contraseña es: {empleado['password']}

        Puedes iniciar sesión en el siguiente enlace:
        {full_login_url}

        Saludos,
        Coordinación de Sistemas CCP
        """

        # Envía el correo
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [empleado["email"]],
            fail_silently=False,
        )
