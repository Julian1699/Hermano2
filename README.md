# Gestión de Productos

Este proyecto es una aplicación web de gestión de productos desarrollada con Flask. Permite a los usuarios crear, leer, actualizar y eliminar (CRUD) productos en una base de datos MySQL, así como gestionar proveedores, bodegas y categorías asociadas a los productos.

## Tecnologías Empleadas

- **Python**: Lenguaje de programación principal.
- **Flask**: Microframework web para Python.
- **Flask-SQLAlchemy**: Extensión para manejar la base de datos con SQLAlchemy.
- **MySQL**: Sistema de gestión de bases de datos relacional.
- **HTML/CSS**: Lenguajes para el diseño de la interfaz de usuario.
- **Jinja2**: Motor de plantillas para Python usado con Flask.

## Funcionalidades del CRUD

- **Crear Producto**: Permite a los usuarios agregar nuevos productos a la base de datos. Requiere la selección de proveedor, bodega y categoría.
- **Leer Productos**: Muestra una lista de todos los productos registrados en la base de datos.
- **Actualizar Producto**: Permite a los usuarios editar la información de los productos existentes.
- **Eliminar Producto**: Permite a los usuarios eliminar productos de la base de datos.
- **Gestionar Proveedores**: Permite a los usuarios agregar, leer, actualizar y eliminar proveedores.
- **Gestionar Bodegas**: Permite a los usuarios agregar, leer, actualizar y eliminar bodegas.
- **Gestionar Categorías**: Permite a los usuarios agregar, leer, actualizar y eliminar categorías.

## Requisitos

- **Docker**
- **Docker Compose**

## Instalación y Configuración

### 1. Clonar el Repositorio

- git clone https://github.com/tu-repositorio.git

- cd nombre-del-repositorio

### 2. Ejecutar Docker Compose

docker-compose up --build

### 3. Acceder a la Aplicación.

La aplicación estará disponible en http://localhost:5000.

### Uso de la Aplicación

### Menú Principal

Al iniciar la aplicación, serás llevado al menú principal, donde podrás gestionar los productos, proveedores, bodegas y categorías. Asegúrate de registrar los proveedores, bodegas y categorías antes de crear un nuevo producto.

## Gestión de Productos

- Crear Producto: Selecciona "Gestionar Productos" y luego "Crear Nuevo Producto". Llena el formulario con los detalles del producto, selecciona el proveedor, bodega y categoría correspondientes, y haz clic en "Registrar Producto".

- Leer Productos: Navega a "Gestionar Productos" para ver una lista de todos los productos registrados.

- Actualizar Producto: En la lista de productos, selecciona "Editar" junto al producto que deseas actualizar. Realiza los cambios necesarios y guarda.

- Eliminar Producto: En la lista de productos, selecciona "Borrar" junto al producto que deseas eliminar.

## Gestión de Proveedores

- Crear Proveedor: Selecciona "Gestionar Proveedores" y luego "Crear Nuevo Proveedor". Llena el formulario con los detalles del proveedor y haz clic en "Registrar Proveedor".

- Leer Proveedores: Navega a "Gestionar Proveedores" para ver una lista de todos los proveedores registrados.

- Actualizar Proveedor: En la lista de proveedores, selecciona "Editar" junto al proveedor que deseas actualizar. Realiza los cambios necesarios y guarda.

- Eliminar Proveedor: En la lista de proveedores, selecciona "Borrar" junto al proveedor que deseas eliminar.

## Gestión de Bodegas

- Crear Bodega: Selecciona "Gestionar Bodegas" y luego "Crear Nueva Bodega". Llena el formulario con los detalles de la bodega y haz clic en "Registrar Bodega".

- Leer Bodegas: Navega a "Gestionar Bodegas" para ver una lista de todas las bodegas registradas.

- Actualizar Bodega: En la lista de bodegas, selecciona "Editar" junto a la bodega que deseas actualizar. Realiza los cambios necesarios y guarda.

- Eliminar Bodega: En la lista de bodegas, selecciona "Borrar" junto a la bodega que deseas eliminar.

## Gestión de Categorías

- Crear Categoría: Selecciona "Gestionar Categorías" y luego "Crear Nueva Categoría". Llena el formulario con los detalles de la categoría y haz clic en "Registrar Categoría".

- Leer Categorías: Navega a "Gestionar Categorías" para ver una lista de todas las categorías registradas.

- Actualizar Categoría: En la lista de categorías, selecciona "Editar" junto a la categoría que deseas actualizar. Realiza los cambios necesarios y guarda.

- Eliminar Categoría: En la lista de categorías, selecciona "Borrar" junto a la categoría que deseas eliminar.

## Consultas y Reportes

El sistema permite consultar la información de productos, proveedores, bodegas y categorías, incluyendo sus detalles y las relaciones entre ellos. Además, se puede calcular el valor total del stock, sumando el precio de cada producto por la cantidad disponible.
