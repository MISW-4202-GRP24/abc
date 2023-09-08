import os
import csv
import json
import requests
import concurrent.futures
from flask import Flask, jsonify

app = Flask(__name__)

# Cargar la configuración desde el archivo config.json
config_file = "config.json"
with open(config_file, 'r') as config:
    config_data = json.load(config)

# Directorio donde se guardarán los registros CSV
LOG_DIR = config_data["LOGS_DIR"]

# Endpoint para enviar las registros
URL = config_data["ATTENDANCE_URL"]

def post_requests():
    with open('candidates.json', 'r') as candidates:
        registers = json.load(candidates)
    
    responses = []


    def send_requests(register):
        response = requests.post(URL, json=register)
        log_request(register, response.status_code) # Registra la solicitud en un archivo CSV
        return response

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_requests, register) for register in registers]
        for future in concurrent.futures.as_completed(futures):
            response = future.result()
            responses.append({
                'status_code': response.status_code
            })

    return jsonify(responses)

# Función para registrar la solicitud en un archivo CSV
def log_request(request_data, status_code):
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, 'requests_log.csv')

    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([json.dumps(request_data), status_code])

if __name__ == '__main__':
    app.run(debug=True)
