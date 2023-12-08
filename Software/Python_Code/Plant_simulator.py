import time
import datetime
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

AWS_IOT_ENDPOINT = "a160q36fslcfae-ats.iot.us-west-2.amazonaws.com"  # change this

# Amazon Root CA 1
AWS_CERT_CA = """-----BEGIN CERTIFICATE-----
                    MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
                    ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
                    b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
                    MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
                    b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
                    ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
                    9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
                    IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
                    VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
                    93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
                    jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
                    AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
                    A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
                    U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
                    N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
                    o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
                    5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
                    rqXRfboQnoZsG4q5WTP468SQvvG5
                    -----END CERTIFICATE-----"""

# Device Certificate (change this)
AWS_CERT_CRT = """-----BEGIN CERTIFICATE-----
                    MIIDWjCCAkKgAwIBAgIVAITY/Jp5+Tp9gmfUl9y5KK9mgw9sMA0GCSqGSIb3DQEB
                    CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
                    IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yMzExMjYxOTA3
                    MDBaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
                    dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCw1mqX1DvqEI2C60tu
                    AZJ0YclxeUgI/LzCPapVg/P/on9DuhAGswTnKu+iK5L6WshpMCw6Qgh01QDyBrpL
                    1t1jZAnk+HKhi0VzxilmI61/+OYKG2uFDX2yoJAuPeh0zwvdZQMWvgQKaKndxJd6
                    SzgXBrQH0ER6BYHyhnYnmse+u2tLfGXXfz2BnwcjJQkDwoBnUh5gOJF12mAPvLEh
                    jxKJZ+bXxM46suQmJjPa0AiptB9tTipS9xJ5CVO9+Tw9dZjSpY/RlGOf57GpHCQZ
                    I9On+ennXwwTnWaGFa0VbdydmVD8r4aQl/X8NGSAWMYFZOwVvEr8iLTb4ttLjeWM
                    QJpxAgMBAAGjYDBeMB8GA1UdIwQYMBaAFPRVqfG2EzHEnOtYb0TAxO1soyXnMB0G
                    A1UdDgQWBBRi+JigTX4maPtHp3fbnE1+e/kbHTAMBgNVHRMBAf8EAjAAMA4GA1Ud
                    DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAjvWyc1Gw2qFhS8tyiuGTxJv1
                    AuwlSVL9nMzs+5JO9qU1lrDF7nZ/PMk/64apZF5W7+dMPl1RcEA/KcqSoV404JfF
                    f5hdD1NIRsDcR8qzE39eMHoyLHPCIj6OhFMEGqxe4rrLrMy0g5YTle5n66QmW74Y
                    f6CZOfLNiyEwdsLpmb77D8+QN3g4JBpZ7Lk94v0XuaRMi4UYQg6yK/8h1UxW2tsL
                    JGi+wCuIxNJfGMr0VlBXLPYcLrXlH6xlSHrQhY2eTgglIpQg4zZxp6wmCPF34Rb9
                    xd+sHRFLvg11pa2Dg5H80u37znjxD6DFEQUxWp4MCaq5IVRTn9SIrYar/IBPRw==
                    -----END CERTIFICATE-----"""

# Device Private Key (change this)
AWS_CERT_PRIVATE = """-----BEGIN RSA PRIVATE KEY-----
                    MIIEowIBAAKCAQEAsNZql9Q76hCNgutLbgGSdGHJcXlICPy8wj2qVYPz/6J/Q7oQ
                    BrME5yrvoiuS+lrIaTAsOkIIdNUA8ga6S9bdY2QJ5PhyoYtFc8YpZiOtf/jmChtr
                    hQ19sqCQLj3odM8L3WUDFr4ECmip3cSXeks4Fwa0B9BEegWB8oZ2J5rHvrtrS3xl
                    1389gZ8HIyUJA8KAZ1IeYDiRddpgD7yxIY8SiWfm18TOOrLkJiYz2tAIqbQfbU4q
                    UvcSeQlTvfk8PXWY0qWP0ZRjn+exqRwkGSPTp/np518ME51mhhWtFW3cnZlQ/K+G
                    kJf1/DRkgFjGBWTsFbxK/Ii02+LbS43ljECacQIDAQABAoIBAQCFZ+yYR/s/NGed
                    iaapAbSb6h2PZoCKjyhTnTPAOcC8bLl3vYlTlIAxaPnJLPg/uHcSq83h0WkRwpNp
                    AtxOVHVGAvVX8HqCFlA57BfVPzsnnPzmSRNPGANo26qJyBhy7rOzvP2cjZL8y0LC
                    1Am2r8JL1LnCX0MZjsgez4OZkzH3V6meDB/muz7GozwsjyNVEGlL+vJGpH1GliM2
                    KmGhoJxv4rgfn1CWMkno9G4OU7P90IRdTumciRwOk/KZWo42KgGF/F05nRdoOxi9
                    49wvBUZAQdDxF7FwBQ7rBwiXMwKZoGDyw3TwW02JIJuPM3NF0+1jXRC9BlCOHC9L
                    PrjQ09pxAoGBANjyt6ATPyXCKm5qPMOdmpqo4GxfvPSFvNtYD5YkNeZ1MVjhT7sJ
                    37hI+7WvizHSYHyRWjsivDdhPQ2EBAiVAhoeCx8Vk+V5WTzMeOZ4RsQPUH6305bu
                    rmFkvGlh/qyJZWtHohQqxGNU669QTgadR2fbu4J+cksvUvFW6t4KPEGtAoGBANCr
                    WNGpNJsHVwweJ3UaFWkW4uno4MoWuDGAh1LMAHWGVT0ZDb/FtJMcGfmvAtxk8cs6
                    FzOLaKa0ZzYcerNLX07XU6hUWWxDtzoyStfrctnE+UwFPkiZsprRQeISE+216y0R
                    cymw2P6i1zRzaAESPS2dUVsT/gmXSZ3lN400C3xVAoGAROrd4FEc507GEetXwECJ
                    w4XQPT0wlnEBrKBN20FHih1CftycamtZkX5Fz9KjIkGVexzlkBGZvvH55hhA+8Ty
                    NP/EQqylHemtqn2+DmC5AkFnLcoRwkmyRagtnkCOGZtQB4Nq/oMTfgaVFE0rbDh8
                    XYbVC0BF6JJxA8+7rquLtsUCgYABk3m9Q6jpDtoidkvX/5Vv0MNv/tlLzXYgsZbU
                    EkRintwf9QN8klK11b2AfEjqPzzwSwUH16K3t58b8oUeu5ABuXChUdnHDo/guaaF
                    EPsyF+HGKDf7NmX582CrA3XxErGvCnWzN+m7qqEzfTeo4mlh4dFOfc0qZ2Ef9y4/
                    O8hmbQKBgFwqXlNILeBcdYbUjLmv/FlFYN7r6y0HuVugVf0TQwPJvhztLQ2R2cAl
                    IMMRD8mWZrTr67kWqrE/g8lNeS525YIRGUWrzgWzYixhZJ/GjnkmvwYBhixgtoyg
                    SLY1KU2SeCNYn20sMVHUWhbUVD3nExKH04OXmrtWSr3s5GIjmSno
                    -----END RSA PRIVATE KEY-----"""


client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./Amazon_CA/AmazonRootCA1.pem', certfile='./Device_Cert/Device_Cert.crt', keyfile='./Private_Key/Private_Key.key', tls_version=ssl.PROTOCOL_SSLv23)
# client.tls_set(ca_certs= AWS_CERT_CA , certfile= AWS_CERT_CRT, keyfile= AWS_CERT_PRIVATE, tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a160q36fslcfae-ats.iot.us-west-2.amazonaws.com", 8883, 60)

# Plant variables
fluid_temperature = 2  # initial temperature
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
            fluid_temperature -= 1
        else:
            fluid_temperature += 1

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

    # timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    # client.publish("raspi/data", payload=json.dumps({"timestamp": timestamp, "distance": distance, "status": status}), qos=0, retain=False)    
    time.sleep(5)

_thread.start_new_thread(simulate_plant, ())
client.loop_forever()

if __name__ == '__main__':
    # Start the plant simulation thread
    plant_simulation_thread = _thread.start_new_thread(simulate_plant, ())

    # Continue with the rest of your program logic or user interaction here if needed

    # Enter the MQTT loop
    client.loop_forever()
