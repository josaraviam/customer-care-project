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
