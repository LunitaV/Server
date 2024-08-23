import subprocess
import re

def update_git_remote_from_codespace():
    try:
        # Ejecutar el comando `gh codespace list` y obtener la salida
        result = subprocess.run(
            ['gh', 'codespace', 'list'],
            capture_output=True, text=True, check=True
        )
        
        # Procesar la salida para extraer el nombre del primer repositorio
        output_lines = result.stdout.splitlines()
        
        if len(output_lines) > 1:
            # La primera línea es el encabezado, la segunda línea es la primera entrada
            repo_line = output_lines[1]
            
            # Buscar la información del repositorio usando una expresión regular
            match = re.search(r'\b(\w+)/(\w+)\b', repo_line)
            
            if match:
                user = match.group(1)
                repo_name = match.group(2)
                
                print(f"Nombre del usuario: {user}")
                print(f"Nombre del repositorio: {repo_name}")
                
                # Establecer la URL del remoto
                remote_url = f"https://github.com/{user}/{repo_name}.git"
                subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)
                print(f"URL remota actualizada a: {remote_url}")
            else:
                print("No se encontró información del repositorio en la línea.")
        else:
            print("No se pudo obtener la información del repositorio.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")

# Ejecutar la función
update_git_remote_from_codespace()
