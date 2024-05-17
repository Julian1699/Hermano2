# Gestión de Productos

Este proyecto es una aplicación web de gestión de productos desarrollada con Flask. Permite a los usuarios crear, leer, actualizar y eliminar (CRUD) productos en una base de datos MySQL.

## Tecnologías Empleadas

- **Python**: Lenguaje de programación principal.
- **Flask**: Microframework web para Python.
- **Flask-SQLAlchemy**: Extensión para manejar la base de datos con SQLAlchemy.
- **MySQL**: Sistema de gestión de bases de datos relacional.
- **HTML/CSS**: Lenguajes para el diseño de la interfaz de usuario.
- **Jinja2**: Motor de plantillas para Python usado con Flask.

## Funcionalidades del CRUD

- **Crear Producto**: Permite a los usuarios agregar nuevos productos a la base de datos.
- **Leer Productos**: Muestra una lista de todos los productos registrados en la base de datos.
- **Actualizar Producto**: Permite a los usuarios editar la información de los productos existentes.
- **Eliminar Producto**: Permite a los usuarios eliminar productos de la base de datos.

## Requisitos

- **Python 3.6+**
- **MySQL**

## Instalación y Configuración

### 1. Clonar el Repositorio

- git clone https://github.com/tu-usuario/nombre-del-repositorio.git

- cd nombre-del-repositorio

2. Crear y Activar un Entorno Virtual

- python -m venv venv

- .\venv\Scripts\activate

3. Instalar las Dependencias

- pip install Flask

- pip install Flask-SQLAlchemy

4. Configurar la Base de Datos

Asegúrate de que MySQL esté instalado y en ejecución. Crea una base de datos llamada hermano2.

- CREATE DATABASE hermano2;

5. Crear las Tablas en la Base de Datos

Ejecuta el script crear_db.py para crear las tablas necesarias en la base de datos.

- python crear_db.py

6. Ejecutar la Aplicación

Finalmente, ejecuta la aplicación Flask.

- python main.py

La aplicación estará disponible en http://127.0.0.1:5000.
