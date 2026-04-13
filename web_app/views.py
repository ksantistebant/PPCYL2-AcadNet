from django.shortcuts import render, redirect
import requests

def subir_notas(request):
    mensaje = ""

    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if archivo:
            archivos_para_flask = {'archivo':(archivo.name, archivo.read(),archivo.content_type)}

            try:
                respuesta = requests.post('http://127.0.0.1:5000/cargar_archivo_notas', files=archivos_para_flask)

                if respuesta.status_code == 200:
                    mensaje = respuesta.json().get('mensaje')
                else:
                    mensaje = f"Error en flask: {respuesta.json().get('error')}"
            except Exception as e:
                mensaje = "Error de conexion. ¿Esta flask encendido?"
        else:
            mensaje = "Por favor selecciona un archivo"
    return render(request, 'subir_notas.html',{'mensaje': mensaje})

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

        if usuario == 'admin' and contrasena == '1234':
            request.session['rol'] = 'admin'
            return redirect('panel_admin')
        
        elif usuario == 'tutor' and contrasena == '123':
            request.session['rol'] = 'tutor'
            return redirect ('subir_notas')
        
        elif usuario.isdigit() and usuario == contrasena:
            request.session['rol'] = 'estudiante'
            request.session['carnet'] = usuario
            return redirect('mis_notas')
        
        else:
            mensaje = "Usuario o contraseña incorrectos"
    return render(request, 'login.html', {'mensaje': mensaje})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def panel_admin(request):
    if request.session.get('rol') != 'admin':
        return redirect('login')
    
    return render(request, 'panel_admin.html')