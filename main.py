from modules.register import register_user
from modules.authenticate import authenticate_user

if __name__ == "__main__":
    option = input("¿Deseas (r)egistrar un nuevo usuario o (a)utenticar un usuario? [r/a]: ")
    
    if option.lower() == 'r':
        name = input("Introduce el nombre del usuario: ")
        register_user(name)
    elif option.lower() == 'a':
        authenticate_user()
    else:
        print("Opción no válida.")
