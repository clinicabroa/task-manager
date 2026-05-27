def format_task(index, task):
    status = "[x]" if task["done"] else "[ ]"
    return f"  {index}. {status} {task['title']}"


def format_task_list(tasks):
    if not tasks:
        return "  (no hay tareas)"
    return "\n".join(format_task(i + 1, t) for i, t in enumerate(tasks))


def format_success(message):
    return f"OK: {message}"


def format_error(message):
    return f"Error: {message}"


def validate_task_title(title):
    title = title.strip()
    if not title:
        return None, "El titulo no puede estar vacio"
    if len(title) > 200:
        return None, "El titulo no puede superar 200 caracteres"
    return title, None


def validate_task_index(value, tasks):
    try:
        index = int(value)
    except ValueError:
        return None, "Debe ingresar un numero"
    if index < 1 or index > len(tasks):
        return None, f"Numero fuera de rango (1-{len(tasks)})"
    return index, None
