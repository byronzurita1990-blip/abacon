#!/usr/bin/env python3
from modulos import GestorTareas, limpiar_pantalla, pausar


def mostrar_menu():
    print("\n" + "=" * 40)
    print("  GESTOR DE TAREAS - KANBAN")
    print("=" * 40)
    print("  1. Ver tablero Kanban")
    print("  2. Ver lista detallada")
    print("  3. Agregar tarea")
    print("  4. Mover tarea")
    print("  5. Editar tarea")
    print("  6. Eliminar tarea")
    print("  7. Estadisticas")
    print("  8. Salir")
    print("=" * 40)


def obtener_columna():
    print("\nColumnas disponibles:")
    print("  1 - Por hacer")
    print("  2 - En progreso")
    print("  3 - Hecho")

    opciones = {"1": "por_hacer", "2": "en_progreso", "3": "hecho"}
    opcion = input("Selecciona columna: ").strip()

    return opciones.get(opcion, "por_hacer")


def main():
    gestor = GestorTareas()

    while True:
        mostrar_menu()
        opcion = input("\nElige una opción: ").strip()

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
            print("--- AGREGAR TAREA ---")
            titulo = input("Título: ").strip()
            if not titulo:
                print("El título no puede estar vacío.")
                pausar()
                continue

            descripcion = input("Descripción (opcional): ").strip()
            columna = obtener_columna()

            exito, mensaje = gestor.agregar_tarea(titulo, descripcion, columna)
            print(f"\n{mensaje}")
            pausar()

        elif opcion == "4":
            limpiar_pantalla()
            print("--- MOVER TAREA ---")
            gestor.mostrar_tareas_detalladas()

            if not gestor.tareas:
                pausar()
                continue

            try:
                indice = input("\nNúmero de tarea a mover: ").strip()
                indice = int(indice)
            except ValueError:
                print("Número inválido.")
                pausar()
                continue

            columna = obtener_columna()
            exito, mensaje = gestor.mover_tarea(indice, columna)
            print(f"\n{mensaje}")
            pausar()

        elif opcion == "5":
            limpiar_pantalla()
            print("--- EDITAR TAREA ---")
            gestor.mostrar_tareas_detalladas()

            if not gestor.tareas:
                pausar()
                continue

            try:
                indice = input("\nNúmero de tarea a editar: ").strip()
                indice = int(indice)
            except ValueError:
                print("Número inválido.")
                pausar()
                continue

            nuevo_titulo = input("Nuevo título (ENTER para mantener): ").strip()
            nueva_descripcion = input("Nueva descripción (ENTER para mantener): ").strip()

            exito, mensaje = gestor.editar_tarea(
                indice,
                nuevo_titulo if nuevo_titulo else None,
                nueva_descripcion if nueva_descripcion else None
            )
            print(f"\n{mensaje}")
            pausar()

        elif opcion == "6":
            limpiar_pantalla()
            print("--- ELIMINAR TAREA ---")
            gestor.mostrar_tareas_detalladas()

            if not gestor.tareas:
                pausar()
                continue

            try:
                indice = input("\nNúmero de tarea a eliminar: ").strip()
                indice = int(indice)
            except ValueError:
                print("Número inválido.")
                pausar()
                continue

            confirmacion = input("¿Estás seguro? (s/n): ").strip().lower()
            if confirmacion == "s":
                exito, mensaje = gestor.eliminar_tarea(indice)
                print(f"\n{mensaje}")
            else:
                print("\nCancelado.")
            pausar()

        elif opcion == "7":
            limpiar_pantalla()
            print("--- ESTADISTICAS ---")
            total, por_columna = gestor.obtener_estadisticas()

            print(f"\nTotal de tareas: {total}")
            for col, cantidad in por_columna.items():
                nombre = gestor.nombres_columnas[col]
                print(f"  {nombre}: {cantidad}")
            pausar()

        elif opcion == "8":
            print("\nHasta luego!")
            break

        else:
            print("\nOpción inválida.")
            pausar()


if __name__ == "__main__":
    main()