from datetime import datetime

# Validar formato de fecha
def validate_date_format(date_string, format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False

# Formatear datos para respuestas de la API
def format_api_response(status, message, data=None):
    response = {
        "status": status,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return response

# Manejar errores en las rutas de la API
def handle_api_error(error):
    print(f"Error ocurrido: {error}")
    return {
        "status": "error",
        "message": str(error)
    }

# Función para validar entradas de texto
def validate_non_empty_string(value, field_name="Campo"):
    if not value or not isinstance(value, str):
        raise ValueError(f"{field_name} no puede estar vacío y debe ser una cadena de texto.")

# Obtener el tiempo actual formateado
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
