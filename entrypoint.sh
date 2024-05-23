#!/bin/sh

# Esperar a que la base de datos esté disponible
echo "Esperando a la base de datos..."

while ! nc -z db-postgres 5432; do
  sleep 0.1
done

echo "Base de datos disponible."

# Ejecutar el script de creación de la base de datos
python crear_db.py

# Iniciar la aplicación Flask
exec "$@"
