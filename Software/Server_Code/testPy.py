import json
import requests
import random
import time

# Function to generate random payload
def generate_random_payload():
    timestamp = int(time.time())
    fluid_temperature = random.uniform(20.0, 100.0)
    heater_status = random.choice([True, False])
    pump1_status = random.choice([True, False])
    pump2_status = random.choice([True, False])
    level_tank1 = random.uniform(0.0, 100.0)
    level_tank2 = random.uniform(0.0, 100.0)

    payload = {
        'timestamp': timestamp,
        'fluid_temperature': fluid_temperature,
        'heater_status': heater_status,
        'pump1_status': pump1_status,
        'pump2_status': pump2_status,
        'level_tank1': level_tank1,
        'level_tank2': level_tank2,
    }

    return payload

# Read payloads from random_payloads.json
with open('random_payloads.json', 'r') as file:
    payloads = json.load(file)

# EC2 server URL
ec2_server_url = 'http://35.166.157.227:8080/setValue'

# Send each payload to the EC2 server
for payload in payloads:
    response = requests.post(ec2_server_url, json=payload)
    print(f"Sent payload: {payload}, Response: {response.status_code}")
    time.sleep(1)  # Add a delay if needed to avoid overwhelming the server
