
import os
from flask import Flask, request, jsonify
from estructuras.matriz_dispersa import MatrizDispersa
from utilidades.lector_xml import procesar_notas_xml

app = Flask(__name__)

matriz_notas = MatrizDispersa()

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'mensaje':'El servidor PPCYL2-AcadNet esta funcionando correctamente'})

@app.route('/consultar_notas_estudiante/<carnet>',methods=['GET'])
def consultar_estudiante(carnet):
    resultado = matriz_notas.obtener_notas_estudiante(carnet)
    return jsonify({"carnet":carnet, "datos": resultado})

@app.route('/consultar_notas_actividad/<actividad>', methods=['GET'])
def consultar_actividad(actividad):
    resultado = matriz_notas.obtener_notas_actividad(actividad)
    return jsonify({"actividad": actividad, "datos":resultado})

@app.route('/cargar_archivo_notas',methods=['POST'])
def cargar_archivo_notas():
    if 'archivo' not in request.files:
        return jsonify({"error":"No se adjunto ningun archivo a la peticion"}), 400
    archivo = request.files['archivo']

    if archivo.filename == '':
        return jsonify({"error": "El nombre del archivo esta vacio"}), 400
    
    if archivo and archivo.filename.endswith('.xml'):
        ruta_temporal = 'temp_notas.xml'

        try:
            archivo.save(ruta_temporal)

            procesar_notas_xml(ruta_temporal,matriz_notas)

            if os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)

            return jsonify({"mensaje": "Archivo procesando y notas cargadas exitosamente"}),200
        except Exception as e:
            return jsonify({"error": f"Ocurrio un error al procesar el archivo: {str(e)}"}),500
    else:
        return jsonify({"error":"El archivo debe tener extension .xml"}),400

if __name__ == '__main__':
    print("Iniciando servidor de PPCYL2-AcadNet en el puerto 500...")
    app.run(debug = True, port=5000)

#print("Iniciando sistema PPCYL2-AcadNet...\n")
#archivo_xml = 'notas_prueba.xml'
#procesar_notas_xml(archivo_xml, matriz_notas)
#print("\n--- Consultando notas ---")
#resultado = matriz_notas.obtener_notas_estudiante("5678")

#print(f"Notas encontradas para el carnet 5678:")
#if type(resultado) == list:
#    for item in resultado:
#        print(f"Actividad: {item['actividad']}, Nota: {item['nota']}")
#else:
#    print(f"{resultado['mensaje']}")

#print("\n--- Consultando notas por actividad ---")
#resultado_actividad = matriz_notas.obtener_notas_actividad("Tarea 1")
#print(f"Notas encontradas para la tarea 1:")
#if type(resultado_actividad) == list:
#    for item in resultado_actividad:
#        print(f"Estudiante: {item['carnet']}, Nota: {item['nota']}")
#else:
#    print(f"{resultado_actividad['mensaje']}")