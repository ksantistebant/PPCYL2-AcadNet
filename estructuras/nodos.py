class Nodo:
    def __init__(self, actividad, carnet, nota):
        # 1. Datos principales
        self.actividad = actividad  # Representa la Fila (ej. "Tarea1")
        self.carnet = carnet        # Representa la Columna (ej. "202301")
        self.nota = nota            # El punteo obtenido
        
        self.arriba = None
        self.abajo = None
        self.izquierda = None
        self.derecha = None

class NodoCabecera:
    def __init__(self, id_cabecera):
        self.id = id_cabecera 
        
        self.siguiente = None
        self.anterior = None
        
        self.acceso = None