# AcadNet - Sistema de Gestión de Notas (PPCYL2)

Este proyecto es una plataforma web robusta diseñada para la gestión y visualización de notas académicas, desarrollada como parte de la formación en **Ingeniería en Análisis de Datos**. Utiliza una arquitectura de microservicios para separar la lógica de procesamiento de datos de la interfaz de usuario.

## 🚀 Estado del Proyecto (v2.0.0 - Versión Final)
El sistema cuenta con una arquitectura núcleo completada y un sistema de gestión integral, permitiendo la comunicación fluida entre el frontend y el backend, con una interfaz de usuario moderna e intuitiva.

### 🌟 Funcionalidades Principales:
* **Sistema de Roles Inteligente:** Dashboards personalizados y enrutamiento dinámico (Post/Redirect/Get) para Administradores, Tutores y Estudiantes.
* **Persistencia Ligera:** Base de datos de usuarios gestionada mediante archivos estructurados (`usuarios.json`).
* **Auditoría y Trazabilidad:** Sistema de bitácora transaccional (`.log`) con interfaz tipo consola para auditar los movimientos del servidor.
* **Procesamiento XML:** Lector automático que valida rangos de notas e integridad de datos.
* **Matriz Dispersa:** Estructura de datos alojada en memoria para el almacenamiento y cálculo eficiente de calificaciones.
* **Diseño UI/UX Profesional:** Interfaz responsiva utilizando variables CSS nativas con una paleta de colores personalizada de alto contraste.

## 🏗️ Arquitectura del Sistema
El sistema se divide en dos servicios principales que interactúan mediante peticiones HTTP:

1. **Servicio Frontend (Django):** Se encarga de la gestión de sesiones, seguridad de rutas, validación de permisos y renderizado de plantillas HTML.
2. **Servicio Backend (Flask - API REST):** Gestiona la memoria RAM del sistema, expone la lógica de la Matriz Dispersa y actúa como motor de procesamiento de archivos.

## 🛠️ Instalación y Ejecución

### Requisitos previos:
* Python 3.x
* Flask
* Django
* Librería `requests`

### Pasos para ejecutar:
1. **Iniciar el Backend (Motor de Datos):**
   ```bash
   python3 app.py

    Iniciar el Frontend (Portal Web en otra terminal):
    Bash

    python3 manage.py runserver 8000

    Acceder: Abre tu navegador de preferencia y ve a http://127.0.0.1:8000/

📊 Historial de Versiones

    v2.0.0 (Versión Actual - Release Candidate):

        Implementación del panel completo de Administrador (Creación de usuarios).

        Integración del sistema de bitácora y monitoreo.

        Refinamiento visual total con CSS y vistas protegidas por rol.

        Persistencia de credenciales e identidades.

    v1.0.0:

        Implementación de arquitectura Cliente-Servidor (Django + Flask).

        Conexión exitosa de módulos de carga de notas y reportes gráficos.

        Sistema de Login básico por sesiones.

👤 Autor

Kat - Desarrollo Integral Backend & Frontend
