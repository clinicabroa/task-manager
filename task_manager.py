from utils import (
    validate_task_title,
    validate_task_index,
    format_task_list,
    format_success,
    format_error,
)

_tasks = []


def add_task(title):
    title, error = validate_task_title(title)
    if error:
        return format_error(error)
    _tasks.append({"title": title, "done": False})
    return format_success(f'Tarea "{title}" agregada')


def list_tasks():
    return format_task_list(_tasks)


def complete_task(index_str):
    if not _tasks:
        return format_error("No hay tareas")
    index, error = validate_task_index(index_str, _tasks)
    if error:
        return format_error(error)
    task = _tasks[index - 1]
    if task["done"]:
        return format_error(f'La tarea "{task["title"]}" ya esta completada')
    task["done"] = True
    return format_success(f'Tarea "{task["title"]}" marcada como completada')


def get_tasks():
    return _tasks
