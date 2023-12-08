import time
import datetime
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
import boto3  # Import the Boto3 library for AWS services

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

# AWS IoT configuration
client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./Amazon_CA/AmazonRootCA1.pem', certfile='./Device_Cert/Device_Cert.crt', keyfile='./Private_Key/Private_Key.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a160q36fslcfae-ats.iot.us-west-2.amazonaws.com", 8883, 60)

# AWS SNS configuration
sns_client = boto3.client('sns')
sns_topic_arn = 'arn:aws:sns:us-west-2:715578268860:IIoT'

# Plant variables (unchanged)
fluid_temperature = 20
heater_status = False
pump1_status = False
pump2_status = False
level_tank1 = 0
level_tank2 = 0
valve1_status = False
valve2_status = False

def simulate_plant():
    global fluid_temperature, heater_status, pump1_status, pump2_status, level_tank1, level_tank2, valve1_status, valve2_status

    while True:
        # Simulate fluid temperature control
        if heater_status:
            fluid_temperature += 1
        else:
            fluid_temperature -= 1

        # Simulate tank1 level control
        if level_tank1 > 50:
            pump1_status = False
        elif level_tank1 < 10:
            pump1_status = True

        # Simulate tank2 level control
        if level_tank2 > 70:
            pump2_status = False
        elif level_tank2 < 30:
            pump2_status = True

        # Simulate drainage from tank1 to tank2
        if valve1_status:
            level_tank1 -= 5
            level_tank2 += 5

        # Simulate drainage from tank2 to reservoir
        if valve2_status:
            level_tank2 -= 5

        # Push data to AWS IoT Core
        push_data_to_iot()

        time.sleep(5)

def push_data_to_iot():
    global fluid_temperature, heater_status, pump1_status, pump2_status, level_tank1, level_tank2, valve1_status, valve2_status

    payload = {
        'fluid_temperature': fluid_temperature,
        'heater_status': heater_status,
        'pump1_status': pump1_status,
        'pump2_status': pump2_status,
        'level_tank1': level_tank1,
        'level_tank2': level_tank2,
        'valve1_status': valve1_status,
        'valve2_status': valve2_status
    }

    timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    client.publish("plant/data", payload=json.dumps({"timestamp": timestamp, **payload}), qos=0, retain=False)

    # Trigger SNS if fluid_temperature > 25
    if fluid_temperature > 25:
        message = f"Alert: Fluid temperature is greater than 25. Current temperature: {fluid_temperature}"
        sns_client.publish(TopicArn=sns_topic_arn, Message=message, Subject="High Fluid Temperature Alert")

    time.sleep(5)

_thread.start_new_thread(simulate_plant, ())
client.loop_forever()

if __name__ == '__main__':
    # Start the plant simulation thread
    plant_simulation_thread = _thread.start_new_thread(simulate_plant, ())

    # Continue with the rest of your program logic or user interaction here if needed

    # Enter the MQTT loop
    client.loop_forever()