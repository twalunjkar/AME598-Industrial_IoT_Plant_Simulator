import json
import random
from datetime import datetime, timedelta

def generate_random_payload():
    timestamp = (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
    fluid_temperature = round(random.uniform(20.0, 100.0), 2)
    heater_status = random.choice([True, False])
    pump1_status = random.choice([True, False])
    pump2_status = random.choice([True, False])
    level_tank1 = round(random.uniform(0.0, 100.0), 2)
    level_tank2 = round(random.uniform(0.0, 100.0), 2)

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

def generate_random_payloads(num_payloads):
    payloads = [generate_random_payload() for _ in range(num_payloads)]
    return payloads

def save_to_json(payloads, filename='random_payloads.json'):
    with open(filename, 'w') as json_file:
        json.dump(payloads, json_file, indent=2)

# Generate 100 random payloads and save to a JSON file
random_payloads = generate_random_payloads(100)
save_to_json(random_payloads)
