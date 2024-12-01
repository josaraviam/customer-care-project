from datetime import datetime


def validate_date_format(date_input, date_format):
    """
    Valida si la entrada es una fecha válida en un formato específico.
    Puede recibir un objeto `datetime` o una cadena.
    """
    if isinstance(date_input, datetime):
        # Si ya es un objeto datetime, validamos su formato convirtiéndolo a string
        date_input = date_input.strftime(date_format)
    try:
        datetime.strptime(date_input, date_format)
        return True
    except ValueError:
        return False


def format_api_response(data, message="Operación exitosa"):
    """
    Formatea la respuesta para las API.
    """
    return {"data": data, "message": message}


def handle_api_error(error):
    """
    Maneja errores y devuelve un formato estándar para respuestas de error.
    """
    return {"error": str(error)}


def generar_id_usuario():
    """
    Genera un ID único para los usuarios en formato 'JXXXX'.
    """
    last_user = usuarios_collection.find_one(sort=[("id_usuario", -1)])
    if not last_user:
        return "J0001"
    last_id = int(last_user["id_usuario"][1:])
    return f"J{last_id + 1:04d}"
