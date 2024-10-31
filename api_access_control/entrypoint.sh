#!/bin/sh

# Espera hasta que la base de datos esté disponible
until python -c "import socket; socket.create_connection(('db', 5432))"; do
    echo "Esperando a que la base de datos esté disponible..."
    sleep 1
done

# Ejecuta las migraciones
echo "Ejecutando migraciones..."
python manage.py migrate

# Si tienes un comando para sembrar empleados, puedes ejecutarlo aquí
echo "Sembrando datos..."
python manage.py seed_employees

# Inicia Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn base.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
