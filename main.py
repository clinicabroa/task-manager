import task_manager


MENU = """
=== Gestor de Tareas ===
1. Agregar tarea
2. Listar tareas
3. Completar tarea
4. Salir
> """


def run():
    while True:
        choice = input(MENU).strip()

        if choice == "1":
            title = input("Titulo de la tarea: ")
            print(task_manager.add_task(title))

        elif choice == "2":
            print("\nTareas:")
            print(task_manager.list_tasks())

        elif choice == "3":
            print("\nTareas:")
            print(task_manager.list_tasks())
            index = input("Numero de tarea a completar: ")
            print(task_manager.complete_task(index))

        elif choice == "4":
            print("Hasta luego.")
            break

        else:
            print("Opcion no valida, elige 1-4")


if __name__ == "__main__":
    run()
