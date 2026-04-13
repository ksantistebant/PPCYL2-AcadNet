import xml.etree.ElementTree as ET

def procesar_notas_xml(ruta_archivo, matriz_dispersa):
    try:
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()

        print(f"-- Iniciando lectura de {ruta_archivo} --")

        for actividad in raiz.iter('actividad'):
            nombre_tarea = actividad.get('nombre')
            carnet_alumno = actividad.get('carnet')

            nota_str = actividad.text

            if nombre_tarea and carnet_alumno and nota_str:
                nota_valor = int(nota_str.strip())

                if 0 <= nota_valor <= 100:
                    matriz_dispersa.insertar_nota(nombre_tarea, carnet_alumno, nota_valor)
                else:
                    print(f"[!]Nota ignorada (fuera de rango): Estudiante {carnet_alumno}, Nota{nota_valor}")

        print("-- Lectura y carga finalizada --")

    except Exception as e:
        print(f"Error al procesar el archivo xml: {e}")