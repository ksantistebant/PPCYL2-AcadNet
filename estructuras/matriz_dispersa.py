from estructuras.nodos import Nodo, NodoCabecera

class MatrizDispersa:
    def __init__(self):
        # Solo necesitamos saber dónde empiezan nuestras cabeceras
        self.inicio_filas = None     # Apuntará a la primera actividad
        self.inicio_columnas = None  # Apuntará al primer carnet
        
    def buscar_fila(self, actividad):
        actual = self.inicio_filas
        while actual is not None:
            if actual.id == actividad:
                return actual
            actual = actual.siguiente
        return None
        
    def buscar_columna(self, carnet):
        actual = self.inicio_columnas
        while actual is not None:
            if actual.id == carnet:
                return actual
            actual = actual.siguiente
        return None
    
#cabeceras
    def crear_fila(self, actividad):
        nueva_fila = NodoCabecera(actividad)

        if self.inicio_filas is None:
            self.inicio_filas = nueva_fila
        else:
            nueva_fila.siguiente = self.inicio_filas
            self.inicio_filas.anterior = nueva_fila
            self.inicio_filas = nueva_fila

        return nueva_fila

    def crear_columna(self, carnet):
        nueva_columna = NodoCabecera(carnet)

        if self.inicio_columnas is None:
            self.inicio_columnas = nueva_columna
        else:
            nueva_columna.siguiente = self.inicio_columnas
            self.inicio_columnas.anterior = nueva_columna
            self.inicio_columnas = nueva_columna

        return nueva_columna

    def insertar_nota(self, actividad, carnet, nota):
        nodo_fila = self.buscar_fila(actividad)

        if nodo_fila is None:
            nodo_fila = self.crear_fila(actividad)

        nodo_columna = self.buscar_columna(carnet)
        if nodo_columna is None:
            nodo_columna = self.crear_columna(carnet)

        nuevo_nodo = Nodo(actividad, carnet, nota)

        if nodo_fila.acceso is None:
            nodo_fila.acceso = nuevo_nodo
        else:
            actual = nodo_fila.acceso
            while actual.derecha is not None:
                actual = actual.derecha
            actual.derecha = nuevo_nodo
            nuevo_nodo.izquierda = actual

        if nodo_columna.acceso is None:
            nodo_columna.acceso = nuevo_nodo
        else:
            actual = nodo_columna.acceso
            while actual.abajo is not None:
                actual = actual.abajo
            actual.abajo = nuevo_nodo
            nuevo_nodo.arriba = actual

        print(f"Nota insertada: Estudiante:{carnet}, Actividad: {actividad}, Nota: {nota}")

    def obtener_notas_estudiante (self, carnet):
        notas_alumno = []

        nodo_columna = self.buscar_columna(carnet)

        if nodo_columna is None:
            return{"mensaje":f"El estudiante {carnet} no tiene ninguna nota registrada"}
        
        actual = nodo_columna.acceso

        while actual is not None:
            notas_alumno.append({"actividad": actual.actividad, "nota": actual.nota})
            actual = actual.abajo
        return notas_alumno
    
    def obtener_notas_actividad(self, actividad):
        notas_actividad = []

        nodo_fila = self.buscar_fila(actividad)

        if nodo_fila is None:
            return{"mensaje":f"La actividad {actividad} no tiene ninguna nota registrada"}
        
        actual = nodo_fila.acceso

        while actual is not None:
            notas_actividad.append({"carnet": actual.carnet, "nota": actual.nota})
            actual = actual.derecha
            
        return notas_actividad