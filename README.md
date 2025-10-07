# Sistema de Gestión de Hotel  

Este proyecto implementa un **sistema de gestión para un hotel** desarrollado en **Python 3.8** utilizando **SQLAlchemy** para la persistencia de datos.  
Incluye autenticación de usuarios, gestión de clientes, habitaciones, reservas y servicios adicionales, todo a través de una interfaz de consola.

---

## Estructura del Proyecto

```
pruebaorm/
│
├── crud/                         
│   ├── habitacion_crud.py
│   ├── reserva_crud.py
│   ├── reserva_servicios_crud.py
│   ├── servicios_adicionales_crud.py
│   ├── tipo_habitacion_crud.py
│   └── usuario_crud.py
│
├── database/                     
│   └── config.py                 
│
├── entities/                     
│   ├── __init__.py
│   ├── habitacion.py
│   ├── reserva_servicios.py
│   ├── reserva.py
│   ├── servicios_adicionales.py
│   ├── tipo_habitacion.py
│   └── usuario.py
│
├── migrations/
│   ├── versions/
│   │   └── 0832f30327b7_create_tables.py
│   ├── env.py
│   └── script.py.mako
│               
├── .env
├── .gitignore 
├── alembic.ini
├── main.py  
├── requirements.txt  
└── README.md                     
```

---

## Requisitos Previos

- **Python 3.8 o superior**  
- **PostgreSQL** (o el motor definido en `database/config.py`)  
- **Dependencias** (instalarlas con el archivo `requirements.txt`):  

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:  
- `sqlalchemy`  
- `psycopg2-binary`  
- `bcrypt` (opcional, para manejo de contraseñas cifradas)

---


### Inicio de Sesión
- El sistema solicitará **nombre de usuario** y **contraseña**.  
- Se permite hasta **3 intentos fallidos** antes de bloquear el acceso.  
- Si es la primera vez, crea un usuario administrador con la opción del menú.

---

## Descripción de la Lógica de Negocio

El sistema cubre los siguientes procesos principales:

### Gestión de Usuarios
- Creación de usuarios (administradores y clientes).  
- Actualización, consulta y eliminación.  
- Cambio de contraseña y actualización de perfil.  

### Gestión de Habitaciones
- Registro de habitaciones con tipo, precio y disponibilidad.  
- Modificación y consulta de estado (disponible, reservada, mantenimiento).  

### Gestión de Reservas
- Creación de reservas asociadas a clientes y habitaciones.  
- Validación de fechas de entrada y salida.  
- Cálculo automático del número de noches y costo total.  
- Control de estados: **confirmada**, **cancelada**, **finalizada**.  

### Servicios Adicionales
- Registro y asociación de servicios (desayuno, spa, transporte, etc.) a una reserva.  
- Suma de costos adicionales a la cuenta final del cliente.  

### Autenticación
- Acceso mediante **nombre de usuario** y contraseña.  
- Distinción de roles:  
  - **Administrador**: acceso completo a todas las gestiones.  
  - **Cliente**: acceso restringido a su perfil y reservas.  

---

## Notas
- La lógica está implementada en la clase `SistemaGestion`, que controla los menús e interacción con el usuario.  
- Todos los accesos a base de datos se hacen mediante objetos CRUD, manteniendo la lógica separada de la persistencia.  
- Se utiliza **SQLAlchemy ORM** para mapear las entidades con la base de datos. 

---

## Cómo Ejecutar el Sistema

1. **Clonar el repositorio**  

```bash
git clone https://github.com/VeronicacortesIsaza/Sistema-Hotel.git
cd Sistema-Hotel
```

2. **Configurar la base de datos**  
   - Crear una base de datos en PostgreSQL.  
   - Ajustar las credenciales en `database/config.py`.  
   - Ejecutar migraciones/creación de tablas:  

   ```bash
   python -m database.config
   ```

3. **Instalar dependencias**  

```bash
pip install -r requirements.txt
```

4. **Ejecutar el sistema**  

```bash
python main.py
```

En consola verás la pantalla de login:

```bash
==================================================
        SISTEMA DE GESTIÓN DE HOTEL
==================================================
INICIAR SESIÓN
==================================================

Intento 1 de 3
Nombre de usuario:
Contraseña:
```
---
