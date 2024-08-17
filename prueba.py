import requests
import subprocess
import re
import time
import json

def load_config():
    with open('configuracion.json', 'r') as file:
        config = json.load(file)
        return config.get('webhook_de_discord')
discord_webhook_url = load_config()
ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


BUFFER_SIZE = 1000

def send_to_discord(message):
    if message.strip(): 
        content = f"```{message}```"
        data = {"content": content}
        response = requests.post(discord_webhook_url, json=data)
        
        if response.status_code == 429:
            retry_after = response.json().get("retry_after", 1)
            time.sleep(retry_after)
            send_to_discord(message)

def run_script():
    process = subprocess.Popen(
        ['python3', 'server.py'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    buffer = []
    started = False
    last_send_time = time.time()
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            if buffer:
                send_to_discord("\n".join(buffer))
            break
        if output:
            cleaned_output = output.strip()
            print(f"{cleaned_output}")
            
            cleaned_output_for_discord = ansi_escape.sub('', cleaned_output)
            
            if "La IP del servidor es:" in cleaned_output_for_discord:
                started = True

            if started:
                buffer.append(cleaned_output_for_discord)
                if len(buffer) > BUFFER_SIZE:
                    send_to_discord("\n".join(buffer))
                    buffer.clear()
                
                current_time = time.time()
                if current_time - last_send_time >= 2:
                    if buffer:
                        send_to_discord("\n".join(buffer))
                        buffer.clear()
                    last_send_time = current_time

        time.sleep(0.1)
if __name__ == "__main__":
    run_script()
