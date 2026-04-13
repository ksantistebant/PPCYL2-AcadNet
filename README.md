# AcadNet - Sistema de Gestión de Notas (PPCYL2)

Este proyecto es una plataforma web robusta diseñada para la gestión y visualización de notas académicas, desarrollada como parte de la formación en **Ingeniería en Análisis de Datos**. Utiliza una arquitectura de microservicios para separar la lógica de procesamiento de datos de la interfaz de usuario.

## 🚀 Estado del Proyecto (v1.0.0)
Actualmente, el sistema cuenta con la arquitectura núcleo completada, permitiendo la comunicación fluida entre el frontend y el backend para la carga y consulta de información.

### Funcionalidades Actuales:
* **Matriz Dispersa:** Estructura de datos personalizada para el almacenamiento eficiente de notas.
* **Procesamiento XML:** Lector automático que valida rangos de notas e integridad de datos.
* **API REST (Flask):** Servicio que expone la lógica de la matriz a través de endpoints seguros.
* **Portal Web (Django):** Interfaz amigable con vistas diferenciadas para Estudiantes y Tutores.
* **Visualización Dinámica:** Generación de reportes gráficos mediante Chart.js.

## 🏗️ Arquitectura del Sistema
El sistema se divide en dos servicios principales:

1. **Servicio 1 (Frontend - Django):** Se encarga de la gestión de sesiones, navegación y renderizado de plantillas HTML.
2. **Servicio 2 (Backend - Flask):** Gestiona la memoria RAM del sistema, donde reside la Matriz Dispersa y el procesador de archivos.

## 🛠️ Instalación y Ejecución

### Requisitos previos:
* Python 3.x
* Flask
* Django
* Librería `requests`

### Pasos para ejecutar:
1. **Iniciar el Backend:**
   ```bash
   python3 app.py

2. **Iniciar el Frontend (en otra terminal):**
    Bash

    python3 manage.py runserver 8000

    Acceder en el navegador a: http://127.0.0.1:8000/

### 📊 Historial de Versiones

    **v1.0.0 (Versión Actual): - Implementación de arquitectura Cliente-Servidor. **

        Conexión exitosa de módulos de carga de notas y reportes gráficos.

        Sistema de Login básico por sesiones.

    **Próximamente (v1.1.0):**

        Implementación del panel completo de Administrador.

        Persistencia de datos (opcional).

        Refinamiento de la interfaz de usuario (CSS avanzado).

### 👤 Autor

    Kat - Desarrollo Integral - [Tu Perfil de GitHub]