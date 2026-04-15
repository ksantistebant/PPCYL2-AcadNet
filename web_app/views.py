from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import datetime
import os
import json

ARCHIVO_USUARIOS = 'usuarios.json'

def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        usuarios_base ={
            "admin": {"contrasena": "1234", "rol": "admin"},
            "tutor": {"contrasena": "1234", "rol": "tutor"}
        }
        with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(usuarios_base, f, indent=4)
        return usuarios_base

    with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def guardar_usuario(usuario, contrasena, rol, nombre):
    usuarios = cargar_usuarios()
    usuarios[usuario] = {
        "contrasena": contrasena, 
        "rol": rol,
        "nombre": nombre
    }
    with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4)

def agregar_usuario(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')
        
    mensaje = ""
    if request.method == 'POST':
        nuevo_usuario = request.POST.get('nuevo_usuario')
        nueva_contra = request.POST.get('nueva_contra')
        nuevo_rol = request.POST.get('nuevo_rol')
        nombre_completo = request.POST.get('nombre_completo') 
        
        usuarios_actuales = cargar_usuarios()
        
        if nuevo_usuario in usuarios_actuales:
            mensaje = f"Error: El usuario '{nuevo_usuario}' ya existe."
        else:
            guardar_usuario(nuevo_usuario, nueva_contra, nuevo_rol, nombre_completo)
            mensaje = f"¡Éxito! Usuario '{nombre_completo}' creado."
            
    return render(request, 'agregar_usuario.html', {'mensaje': mensaje})

def registrar_movimiento(usuario, accion):
    fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensaje = f"[{fecha_hora}] Usuario: {usuario} | Accion: {accion}"

    with open('bitacora.log','a', encoding='utf-8') as archivo:
        archivo.write(mensaje)

def subir_notas(request):
    # 1. El nuevo portero: Deja pasar tanto a 'admin' como a 'tutor'
    rol_actual = request.session.get('rol')
    if rol_actual not in ['admin', 'tutor']:
        return redirect('login')

    mensaje = ""

    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if archivo:
            archivos_para_flask = {'archivo': (archivo.name, archivo.read(), archivo.content_type)}

            try:
                respuesta = requests.post('http://127.0.0.1:5000/cargar_archivo_notas', files=archivos_para_flask)

                if respuesta.status_code == 200:
                    messages.success(request, '¡Archivo procesado y notas cargadas exitosamente!')
                    registrar_movimiento(request.session.get('usuario'), 'Cargó un nuevo archivo XML de notas')
                    
                    if rol_actual == 'admin':
                        return redirect('panel_admin')
                    else:
                        return redirect('panel_tutor')
                        
                else:
                    mensaje = f"Error en flask: {respuesta.json().get('error')}"
            except Exception as e:
                mensaje = "Error de conexión. ¿Está flask encendido?"
        else:
            mensaje = "Por favor selecciona un archivo"
            
    return render(request, 'subir_notas.html', {'mensaje': mensaje})

def mis_notas(request):
    datos_notas = None
    mensaje = ""
    carnet_buscado = ""

    if request.method == 'POST':
        carnet_buscado = request.POST.get('carnet')

        if carnet_buscado:
            try:
                url = f"http://127.0.0.1:5000/consultar_notas_estudiante/{carnet_buscado}"
                respuesta = requests.get(url)

                if respuesta.status_code == 200:
                    data = respuesta.json()

                    if type(data.get('datos')) == list:
                        datos_notas = data.get('datos')
                    else:
                        mensaje = data.get('datos').get('mensaje')

                else:
                    mensaje = "Error al consultar la API"

            except Exception as e:
                mensaje = "Error de conexion con el servidor Flask"

    return render(request, 'mis_notas.html', {
            'datos_notas': datos_notas,
            'mensaje': mensaje,
            'carnet': carnet_buscado
        })

def reporte_tutor(request):
    datos_actividad = None
    mensaje = ""
    actividad_buscada = ""

    etiquetas_grafica = []
    datos_grafica = []

    if request.method == 'POST':
        actividad_buscada = request.POST.get('actividad')

        if actividad_buscada:
            try:
                url = f'http://127.0.0.1:5000/consultar_notas_actividad/{actividad_buscada}'
                respuesta = requests.get(url)

                if respuesta.status_code == 200:
                    data = respuesta.json()
                    if type(data.get('datos')) == list:
                        datos_actividad = data.get('datos')

                        for item in datos_actividad:
                            etiquetas_grafica.append(item['carnet'])
                            datos_grafica.append(int(item['nota']))
                    else:
                        mensaje = data.get('datos').get('mensaje')
                else:
                    mensaje = "Error al consultar la API"
            except Exception as e:
                mensaje = "Error de conexion con el servidor flask"
    return render(request,'reporte_tutor.html',{
        'datos_actividad': datos_actividad,
        'mensaje': mensaje,
        'actividad': actividad_buscada,
        'etiquetas_grafica': etiquetas_grafica,
        'datos_grafica': datos_grafica
    })

def login_view(request):
    mensaje = ""

    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        
        usuarios = cargar_usuarios()
        
        if usuario in usuarios and usuarios[usuario]['contrasena'] == contrasena:
            rol = usuarios[usuario]['rol']
            
            request.session['rol'] = rol
            request.session['usuario'] = usuario 
            
            registrar_movimiento(usuario, 'Inició sesión')
            
            if rol == 'admin':
                return redirect('panel_admin')
            elif rol == 'tutor':
                return redirect('panel_tutor')
            elif rol == 'estudiante':
                request.session['carnet'] = usuario
                return redirect('panel_estudiante')
                
        elif usuario.isdigit() and usuario == contrasena:
            request.session['rol'] = 'estudiante'
            request.session['carnet'] = usuario
            return redirect('panel_estudiante')
            
        else:
            mensaje = "Usuario o contraseña incorrectos."
            
    return render(request, 'login.html', {'mensaje': mensaje})

def logout_view(request):
    registrar_movimiento(request.session.get('usuario'),'Cerro sesion')
    request.session.flush()
    return redirect('login')

def panel_admin(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')
    
    return render(request, 'panel_admin.html')

def ver_bitacora(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')

    historial = []
    if os.path.exists('bitacora.log'):
        with open('bitacora.log', 'r', encoding='utf-8') as archivo:
            # strip() limpia espacios extra y \n, para tener las líneas limpias
            historial = [linea.strip() for linea in archivo.readlines() if linea.strip()] 
            # Le damos la vuelta para ver lo más reciente primero
            historial = historial[::-1]
    else:
        historial.append("No hay registros en la bitácora todavía.")

    return render(request, 'bitacora.html', {'historial': historial})

def agregar_usuario(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')
        
    mensaje = ""
    
    if request.method == 'POST':
        nuevo_usuario = request.POST.get('nuevo_usuario')
        nueva_contra = request.POST.get('nueva_contra')
        nuevo_rol = request.POST.get('nuevo_rol')
        
        nombre_completo = request.POST.get('nombre_completo') 
        
        usuarios_actuales = cargar_usuarios()
        
        if nuevo_usuario in usuarios_actuales:
            mensaje = f"Error: El usuario '{nuevo_usuario}' ya existe."
        else:
            guardar_usuario(nuevo_usuario, nueva_contra, nuevo_rol, nombre_completo)
            
            registrar_movimiento('Admin', f'Creó al usuario {nombre_completo} con rol {nuevo_rol}')
            
            mensaje = f"¡Éxito! El {nuevo_rol} '{nombre_completo}' ha sido creado."
            
    return render(request, 'agregar_usuario.html', {'mensaje': mensaje})

def panel_tutor(request):
    if request.session.get('rol') != 'tutor':
        return redirect('login')
    return render(request, 'panel_tutor.html')

def panel_estudiante(request):
    if request.session.get('rol') != 'estudiante':
        return redirect('login')
    
    carnet = request.session.get('usuario')
    usuarios = cargar_usuarios()
    
    datos_usuario = usuarios.get(carnet, {})
    nombre = datos_usuario.get('nombre', 'Estudiante')
    
    return render(request, 'panel_estudiante.html', {
        'carnet': carnet,
        'nombre': nombre
    })  
