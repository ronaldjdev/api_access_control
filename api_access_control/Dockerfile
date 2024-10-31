# Usa la imagen oficial de Python 3.12.7 como base
FROM python:3.12.7

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y el código de tu aplicación al contenedor
COPY requirements.txt /app/
COPY . /app/

RUN chmod +x /app/entrypoint.sh
# Instala las dependencias de tu aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que va a usar Gunicorn
EXPOSE 8000

# Comando para iniciar Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "base.wsgi:application"]
