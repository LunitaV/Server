import os
import json
import requests

def get_current_branch():
    # Obtener el nombre de la rama actual
    branch_name = os.popen('git branch --show-current').read().strip()
    return branch_name

def repo_exists(token, account_name, repo_name):
    # Verificar si el repositorio ya existe
    response = requests.get(
        f'https://api.github.com/repos/{account_name}/{repo_name}',
        headers={'Authorization': f'token {token}'}
    )
    return response.status_code == 200 
def create_repo(token, account_name, repo_name, repo_private):
    # Crear el repositorio en GitHub
    data = json.dumps({
        'name': repo_name,
        'private': repo_private
    })
    response = requests.post(
        'https://api.github.com/user/repos',
        headers={
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        },
        data=data
    )
    if response.status_code == 201:
        print("Repositorio creado exitosamente.")
    else:
        print(f"Error al crear el repositorio: {response.json()}")

def push_to_repo(token, account_name, repo_name):
    # Configurar el origen remoto y hacer push
    remote_url = f'https://{token}@github.com/{account_name}/{repo_name}.git'
    os.system(f'git remote add origin {remote_url}')
    
    # Hacer push a la rama actual
    branch_name = get_current_branch()
    os.system(f'git push -u origin {branch_name}')

def create_or_update_repo():
    # Pedir el token de acceso
    token = input("Introduce tu token de acceso personal de GitHub: ")
    
    # Constantes
    repo_name = "Minecraft_branch"
    repo_private = "no"# Cambiado de "sí/no" a "true/false"# Pedir el nombre de la cuenta de GitHub
    account_name = input("Introduce el nombre de la cuenta de GitHub donde deseas usar el repositorio: ")

    # Verificar si el repositorio ya existe
    if repo_exists(token, account_name, repo_name):
        print("El repositorio ya existe. Empujando archivos al repositorio existente.")
    else:
        print("El repositorio no existe. Creando un nuevo repositorio.")
        create_repo(token, account_name, repo_name, repo_private.lower() == 'sí')

    # Inicializar el repositorio localmente en el Codespace
    os.system('git init')

    # Añadir archivos y hacer commit
    os.system('git add .')
    os.system('git commit -m "Primer commit desde Codespace"')

    # Hacer push a la rama actual
    push_to_repo(token, account_name, repo_name)

if __name__ == "__main__":
    create_or_update_repo()
