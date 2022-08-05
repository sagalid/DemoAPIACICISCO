import json
import requests
import conf

sandbox = "https://sandboxapicdc.cisco.com"


def obtener_token(usuario, clave):
    url = sandbox + "/api/aaaLogin.json"
    body = {
        "aaaUser": {
            "attributes": {
                "name": usuario,
                "pwd": clave
            }
        }
    }
    cabecera = {
        "Content-Type": "application/json"
    }
    requests.packages.urllib3.disable_warnings()
    respuesta = requests.post(url, headers=cabecera, data=json.dumps(body), verify=False)
    token = respuesta.json()['imdata'][0]['aaaLogin']['attributes']['token']
    return token


# GET http://apic-ip-address/api/class/topSystem.json

def top_system():
    cabecera = {
        "Content-Type": "application/json"
    }
    galleta = {
        "APIC-Cookie": obtener_token(conf.usuario, conf.clave)
    }

    requests.packages.urllib3.disable_warnings()

    try:
        respuesta = requests.get(sandbox+"/api/class/topSystem.json", headers=cabecera, cookies=galleta, verify=False)
        print(respuesta.request.method)
        print(respuesta.request.path_url)
        print(respuesta.request.body)
        print(respuesta.request.headers['Cookie'])
        print(respuesta.headers)
    except Exception as err:
        print("Error al consumir el API por problemas de conexion")
        exit(1)

    total_nodos = int(respuesta.json()["totalCount"])

    for i in range(0, total_nodos):
        ip_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["address"]
        mac_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["fabricMAC"]
        state_local = respuesta.json()["imdata"][i]["topSystem"]["attributes"]["state"]

        print(ip_local + "|" + mac_local + "|" + state_local)

top_system()


