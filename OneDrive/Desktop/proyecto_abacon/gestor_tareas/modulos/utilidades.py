import os
import sys
import json
from pathlib import Path


def obtener_ruta_datos():
    base_dir = Path(__file__).parent.parent
    return base_dir / "datos" / "tareas.json"


def cargar_datos():
    ruta = obtener_ruta_datos()
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "tareas": [],
            "columnas": ["por_hacer", "en_progreso", "hecho"],
            "nombre_columnas": {
                "por_hacer": "Por hacer",
                "en_progreso": "En progreso",
                "hecho": "Hecho"
            }
        }


def guardar_datos(datos):
    ruta = obtener_ruta_datos()
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def validar_titulo(titulo):
    if not titulo or not titulo.strip():
        return False, "El título no puede estar vacío"
    if len(titulo.strip()) > 100:
        return False, "El título no puede exceder 100 caracteres"
    return True, ""


def validar_descripcion(descripcion):
    if len(descripcion) > 500:
        return False, "La descripción no puede exceder 500 caracteres"
    return True, ""


def validar_columna(columna, columnas_validas):
    if columna not in columnas_validas:
        return False, f"Columna inválida. Opciones: {', '.join(columnas_validas)}"
    return True, ""


def validar_indice_tarea(indice, max_indice):
    try:
        indice = int(indice)
        if indice < 1 or indice > max_indice:
            return False, f"Índice debe estar entre 1 y {max_indice}"
        return True, indice - 1
    except ValueError:
        return False, "Debes ingresar un número válido"


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresiona ENTER para continuar...")


def generar_id_tarea(tareas):
    if not tareas:
        return 1
    return max(t["id"] for t in tareas) + 1


def formatear_fecha(fecha_iso):
    from datetime import datetime
    try:
        fecha = datetime.fromisoformat(fecha_iso.replace("Z", "+00:00"))
        return fecha.strftime("%d/%m/%Y %H:%M")
    except:
        return fecha_iso


def obtener_fecha_actual():
    from datetime import datetime
    return datetime.now().isoformat()