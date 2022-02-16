from utn_tools.tgm import emojis

COMMAND_NOT_FOUND_MESSAGE = f"""No entiendo lo que intentas decir {emojis.DOWNCAST_FACE_WITH_SWEAT}\\. \
Utiliza el comando /help para que ver mas información acerca de lo que puedo hacer por ti\\!"""


def get_help_message(command_name: str):
    return f"""
**Hola**, soy el bot de encuestas de la UTN\\-FRM\\ {emojis.SMILING_FACE_WITH_SUNGLASSES}

Para comenzar solo tenés que mandar el siguiente mensaje\\:

`{command_name} \\<dni\\> \\<legajo\\> \\<contraseña\\>`
"""


def get_surveys_completed_message(username: str, surveys_completed: int):
    if surveys_completed:
        return f"{username}\\, he completado {surveys_completed} encuestas {emojis.FIRE}\\."

    else:
        return f"""{username}, no he encontrado encuestas sin responder {emojis.CONFUSED_FACE}\\."""


def get_login_error_message(dni: int, legajo: int, password: str):
    return f"""No pude iniciar sesión en tu cuenta\\. Verifica que los datos ingresados \
sean correctos\\:
```
- dni: {dni}
- legajo: {legajo}
- contraseña: {password}
```"""
