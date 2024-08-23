# main.py

from modules.authenticate import authenticate_user  # Importa la función para autenticar usuarios
from modules.register import register_user  # Importa la función para registrar nuevos usuarios

def main():
    # Pregunta al usuario si desea registrar un nuevo usuario o autenticar uno existente
    action = input("¿Deseas (r)egistrar un nuevo usuario o (a)utenticar un usuario? [r/a]: ").strip().lower()

    if action == 'r':
        # Registrar un nuevo usuario
        name = input("Introduce el nombre del usuario: ").strip()
        register_user(name)
    elif action == 'a':
        # Autenticar un usuario existente
        authenticate_user()
    else:
        print("Acción no reconocida. Por favor, elige 'r' para registrar o 'a' para autenticar.")

if __name__ == "__main__":
    main()
