# Usar una imagen base de Python
FROM python:3.9

# Instalar netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del proyecto en el contenedor
COPY . .

# Copiar el script de entrada
COPY entrypoint.sh /entrypoint.sh

# Hacer ejecutable el script de entrada
RUN chmod +x /entrypoint.sh

# Exponer el puerto 5000 para Flask
EXPOSE 5000

# Comando de inicio
ENTRYPOINT ["/entrypoint.sh"]
