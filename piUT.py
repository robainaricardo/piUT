# Bibliotecas
import Adafruit_DHT
import datetime
import time
from pymongo import MongoClient


# Constantes
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
INTERVALO = 30
ARQUIVO = "temperatura.log"
BD = "mongodb+srv://tchelinux:tchelinux1234@cluster0.vfev4.mongodb.net/<dbname>?retryWrites=true&w=majority"
SENSOR = "bage-0001"


# Funções
def salvarLog(umidade, temperatura, data):
    with open(ARQUIVO, 'a') as log:
        log.write(f"Sensor: {SENSOR}, Data: {data}, Umidade: {umidade}, Temperatura: {temperatura}\n")


def salvarBD(umidade, temperatura, data):
    client = MongoClient(BD)
    db = client.tchelinux
    db.piUT.insert_one({"Sensor" : SENSOR, "data": data, "umidade": umidade, "temperatura": temperatura})


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
