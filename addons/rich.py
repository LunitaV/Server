import os

def create_repo_in_another_account():
    # Pedir los datos necesarios
    token = input("Introduce tu token de acceso personal de GitHub: ")
    repo_name = "Minecraft_branch"
    repo_private = "no"
    account_name = input("Introduce el nombre de la cuenta de GitHub donde deseas crear el repositorio: ")

    # Crear el repositorio en la otra cuenta de GitHub
    create_repo_command = f'curl -H "Authorization: token {token}" https://api.github.com/user/repos -d \'{{"name":"{repo_name}", "private":{str(repo_private).lower()}}}\''
    os.system(create_repo_command)

    # Inicializar el repositorio localmente en el Codespace
    os.system('git init')

    # Añadir archivos y hacer commit
    os.system('git add .')
    os.system('git commit -m "Primer commit desde Codespace"')

    # Configurar el origen remoto y hacer push
    remote_url = f'https://{token}@github.com/{account_name}/{repo_name}.git'
    os.system(f'git remote add origin {remote_url}')
    os.system('git push -u origin master')

if __name__ == "__main__":
    create_repo_in_another_account()