from .utilidades import (
    cargar_datos,
    guardar_datos,
    validar_titulo,
    validar_descripcion,
    validar_columna,
    validar_indice_tarea,
    generar_id_tarea,
    obtener_fecha_actual,
    formatear_fecha
)


class GestorTareas:
    def __init__(self):
        self.datos = cargar_datos()
        self.tareas = self.datos["tareas"]
        self.columnas = self.datos["columnas"]
        self.nombres_columnas = self.datos["nombre_columnas"]

    def guardar(self):
        self.datos["tareas"] = self.tareas
        guardar_datos(self.datos)

    def agregar_tarea(self, titulo, descripcion="", columna="por_hacer"):
        valido, mensaje = validar_titulo(titulo)
        if not valido:
            return False, mensaje

        valido, mensaje = validar_descripcion(descripcion)
        if not valido:
            return False, mensaje

        valido, mensaje = validar_columna(columna, self.columnas)
        if not valido:
            return False, mensaje

        nueva_tarea = {
            "id": generar_id_tarea(self.tareas),
            "titulo": titulo.strip(),
            "descripcion": descripcion.strip(),
            "columna": columna,
            "creada": obtener_fecha_actual(),
            "actualizada": obtener_fecha_actual()
        }

        self.tareas.append(nueva_tarea)
        self.guardar()
        return True, f"Tarea '{titulo}' agregada en '{self.nombres_columnas[columna]}'"

    def listar_tareas(self, columna=None):
        if columna:
            return [t for t in self.tareas if t["columna"] == columna]
        return self.tareas

    def mover_tarea(self, indice, nueva_columna):
        valido, mensaje = validar_indice_tarea(indice, len(self.tareas))
        if not valido:
            return False, mensaje

        valido, mensaje = validar_columna(nueva_columna, self.columnas)
        if not valido:
            return False, mensaje

        self.tareas[indice]["columna"] = nueva_columna
        self.tareas[indice]["actualizada"] = obtener_fecha_actual()
        self.guardar()
        return True, f"Tarea movida a '{self.nombres_columnas[nueva_columna]}'"

    def editar_tarea(self, indice, nuevo_titulo=None, nueva_descripcion=None):
        valido, mensaje = validar_indice_tarea(indice, len(self.tareas))
        if not valido:
            return False, mensaje

        if nuevo_titulo:
            valido, mensaje = validar_titulo(nuevo_titulo)
            if not valido:
                return False, mensaje
            self.tareas[indice]["titulo"] = nuevo_titulo.strip()

        if nueva_descripcion is not None:
            valido, mensaje = validar_descripcion(nueva_descripcion)
            if not valido:
                return False, mensaje
            self.tareas[indice]["descripcion"] = nueva_descripcion.strip()

        self.tareas[indice]["actualizada"] = obtener_fecha_actual()
        self.guardar()
        return True, "Tarea actualizada"

    def eliminar_tarea(self, indice):
        valido, mensaje = validar_indice_tarea(indice, len(self.tareas))
        if not valido:
            return False, mensaje

        titulo = self.tareas[indice]["titulo"]
        del self.tareas[indice]
        self.guardar()
        return True, f"Tarea '{titulo}' eliminada"

    def obtener_tareas_por_columna(self):
        resultado = {}
        for col in self.columnas:
            resultado[col] = [t for t in self.tareas if t["columna"] == col]
        return resultado

    def mostrar_tablero(self):
        print("\n" + "=" * 50)
        print("TABLERO KANBAN".center(50))
        print("=" * 50)

        tareas_por_col = self.obtener_tareas_por_columna()

        for columna in self.columnas:
            nombre = self.nombres_columnas[columna]
            tareas = tareas_por_col[columna]

            print(f"\n--- {nombre} ({len(tareas)}) ---")
            if not tareas:
                print("  (sin tareas)")
            else:
                for i, tarea in enumerate(tareas, 1):
                    print(f"  {i}. {tarea['titulo']}")

    def mostrar_tareas_detalladas(self, columna=None):
        print("\n" + "=" * 50)
        print("LISTA DE TAREAS".center(50))
        print("=" * 50)

        tareas = self.listar_tareas(columna)

        if not tareas:
            print("\nNo hay tareas todavía.")
            return

        for i, tarea in enumerate(tareas, 1):
            nombre_col = self.nombres_columnas[tarea["columna"]]
            print(f"\n[{i}] {tarea['titulo']}")
            print(f"    Estado: {nombre_col}")
            if tarea.get("descripcion"):
                print(f"    Descripción: {tarea['descripcion']}")
            print(f"    Creada: {formatear_fecha(tarea['creada'])}")
            print(f"    Actualizada: {formatear_fecha(tarea['actualizada'])}")

    def obtener_estadisticas(self):
        total = len(self.tareas)
        por_columna = {}
        for col in self.columnas:
            por_columna[col] = len([t for t in self.tareas if t["columna"] == col])

        return total, por_columna