#!/usr/bin/env python3
from modulos import (
    GestorTareas, limpiar_pantalla, pausar,
    VERDE, ROJO, AMARILLO, AZUL, MAGENTA, NEGRITA, RESET
)


def mostrar_menu():
    print(f"\n{AZUL}{'=' * 40}")
    print(f"{NEGRITA}  GESTOR DE TAREAS - KANBAN{RESET}")
    print(f"{AZUL}{'=' * 40}")
    print(f"  {MAGENTA}1.{RESET} Ver tablero Kanban")
    print(f"  {MAGENTA}2.{RESET} Ver lista detallada")
    print(f"  {MAGENTA}3.{RESET} Agregar tarea")
    print(f"  {MAGENTA}4.{RESET} Mover tarea")
    print(f"  {MAGENTA}5.{RESET} Editar tarea")
    print(f"  {MAGENTA}6.{RESET} Eliminar tarea")
    print(f"  {MAGENTA}7.{RESET} Estadisticas")
    print(f"  {MAGENTA}8.{RESET} Salir")
    print(f"{AZUL}{'=' * 40}")


def obtener_columna():
    print(f"\n{AMARILLO}Columnas disponibles:{RESET}")
    print(f"  {MAGENTA}1{RESET} - Por hacer")
    print(f"  {MAGENTA}2{RESET} - En progreso")
    print(f"  {MAGENTA}3{RESET} - Hecho")

    opciones = {"1": "por_hacer", "2": "en_progreso", "3": "hecho"}
    opcion = input("Selecciona columna: ").strip()

    return opciones.get(opcion, "por_hacer")


def obtener_tarea_seleccionada(gestor, indice):
    """Devuelve la tarea seleccionada o None si es inválido."""
    try:
        indice = int(indice)
        if indice < 1 or indice > len(gestor.tareas):
            return None
        return gestor.tareas[indice - 1]
    except ValueError:
        return None


def confirmar_accion(titulo, accion):
    """Confirmación robusta que muestra el título de la tarea."""
    print(f"\n{AMARILLO}¿{accion} '{titulo}'?{RESET}")
    print(f"  Escribe {MAGENTA}s{RESET} para confirmar o cualquier cosa para cancelar")
    confirmacion = input("> ").strip().lower()
    return confirmacion == "s"


def main():
    gestor = GestorTareas()

    while True:
        mostrar_menu()
        opcion = input(f"\n{AZUL}Elige una opcion:{RESET} ").strip()

        if opcion == "1":
            limpiar_pantalla()
            gestor.mostrar_tablero()
            pausar()

        elif opcion == "2":
            limpiar_pantalla()
            gestor.mostrar_tareas_detalladas()
            pausar()

        elif opcion == "3":
            limpiar_pantalla()
            print(f"{AZUL}--- AGREGAR TAREA ---{RESET}")
            titulo = input(f"{AMARILLO}Titulo:{RESET} ").strip()
            if not titulo:
                print(f"\n{ROJO}El titulo no puede estar vacio.{RESET}")
                pausar()
                continue

            descripcion = input(f"{AMARILLO}Descripcion (opcional):{RESET} ").strip()
            columna = obtener_columna()

            exito, mensaje = gestor.agregar_tarea(titulo, descripcion, columna)
            print(f"\n{VERDE}{mensaje}{RESET}")
            pausar()

        elif opcion == "4":
            limpiar_pantalla()
            print(f"{AZUL}--- MOVER TAREA ---{RESET}")
            gestor.mostrar_tareas_detalladas()

            if not gestor.tareas:
                pausar()
                continue

            indice = input(f"\n{AMARILLO}Numero de tarea a mover:{RESET} ").strip()
            tarea = obtener_tarea_seleccionada(gestor, indice)

            if not tarea:
                print(f"\n{ROJO}Numero invalido.{RESET}")
                pausar()
                continue

            print(f"\n{VERDE}Tarea seleccionada: '{tarea['titulo']}'{RESET}")
            columna = obtener_columna()

            exito, mensaje = gestor.mover_tarea(int(indice), columna)
            print(f"\n{VERDE}{mensaje}{RESET}")
            pausar()

        elif opcion == "5":
            limpiar_pantalla()
            print(f"{AZUL}--- EDITAR TAREA ---{RESET}")
            gestor.mostrar_tareas_detalladas()

            if not gestor.tareas:
                pausar()
                continue

            indice = input(f"\n{AMARILLO}Numero de tarea a editar:{RESET} ").strip()
            tarea = obtener_tarea_seleccionada(gestor, indice)

            if not tarea:
                print(f"\n{ROJO}Numero invalido.{RESET}")
                pausar()
                continue

            print(f"\n{VERDE}Editando: '{tarea['titulo']}'{RESET}")
            nuevo_titulo = input(f"{AMARILLO}Nuevo titulo (ENTER para mantener):{RESET} ").strip()
            nueva_descripcion = input(f"{AMARILLO}Nueva descripcion (ENTER para mantener):{RESET} ").strip()

            exito, mensaje = gestor.editar_tarea(
                indice,
                nuevo_titulo if nuevo_titulo else None,
                nueva_descripcion if nueva_descripcion else None
            )
            print(f"\n{VERDE}{mensaje}{RESET}")
            pausar()

        elif opcion == "6":
            limpiar_pantalla()
            print(f"{AZUL}--- ELIMINAR TAREA ---{RESET}")
            gestor.mostrar_tareas_detalladas()

            if not gestor.tareas:
                pausar()
                continue

            indice = input(f"\n{AMARILLO}Numero de tarea a eliminar:{RESET} ").strip()
            tarea = obtener_tarea_seleccionada(gestor, indice)

            if not tarea:
                print(f"\n{ROJO}Numero invalido.{RESET}")
                pausar()
                continue

            if confirmar_accion(tarea['titulo'], "Eliminar"):
                exito, mensaje = gestor.eliminar_tarea(int(indice))
                print(f"\n{ROJO}{mensaje}{RESET}")
            else:
                print(f"\n{AMARILLO}Cancelado.{RESET}")
            pausar()

        elif opcion == "7":
            limpiar_pantalla()
            print(f"{AZUL}--- ESTADISTICAS ---{RESET}")
            total, por_columna, grafico = gestor.obtener_estadisticas()

            print(f"\n{AZUL}Total de tareas: {NEGRITA}{total}{RESET}")
            print(f"\n{grafico}")
            pausar()

        elif opcion == "8":
            print(f"\n{AZUL}Hasta luego!{RESET}")
            break

        else:
            print(f"\n{ROJO}Opcion invalida.{RESET}")
            pausar()


if __name__ == "__main__":
    main()