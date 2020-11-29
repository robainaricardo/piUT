# Bibliotecas
import Adafruit_DHT
import datetime
import time
from pymongo import MongoClient

# Constantes
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
INTERVALO = 30
ARQUIVO = "/var/log/temperatura"
BD_IP = "192.168.122.1"
BD_PORTA = "27017"
SENSOR = "bage-0001"

# Main
while True:
    # Recebe a medição feita pelo sensor e a data
    umidade, temperatura = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    data = datetime.datetime.now()

    # Verifica se a medição é válida
    if umidade is not None and temperatura is not None:
        # Imprime o valore recebido
        print(f"Sensor: {SENSOR}, Data: {data}, Umidade: {umidade}, Temperatura: {temperatura}\n")

        # Salva a medição em um Log
        salvarLog(umidade, temperatura, data)

        # Salva a medição no banco de dados
        salvarBD(umidade, temperatura, data)

        # Espera 30 segundos antes de realizar a proxima coleta
        time.sleep(INTERVALO)
    else:
        # Erro ao realizar a medição, tenta novamente
        print("Medição inválida")

# Funções
def salvarLog(umidade, temperatura, data):
    with open(ARQUIVO, 'w') as log:
        log.write(f"Sensor: {SENSOR}, Data: {data}, Umidade: {umidade}, Temperatura: {temperatura}\n")


def salvarBD(umidade, temperatura, data):
    client = MongoClient(BD_IP, BD_PORTA)
    db = client.temperatura
    medicao = db.insert_one({"Sensor" : SENSOR, "data": data, "umidade": umidade, "temperatura": temperatura}).inserted_id()


