import pika
from pika.exchange_type import ExchangeType
import time
import csv
import json
from dotenv import load_dotenv
import os
from multiprocessing import Process

load_dotenv(override=True)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST") 

class IqaSensor:
    def __init__(self):
        self.__connection = None
        self.__channel = None
        self.__time = 5
        self.__data = []
        self.__id = None

    def create_connection(self, host: str) -> None:
        connection_parameters = pika.ConnectionParameters(host)
        self.__connection = pika.BlockingConnection(connection_parameters)
        self.__channel = self.__connection.channel()  
        self.__channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

    def read_csv(self, file_path: str):
        self.__id = file_path.split("/")[1].split(".")[0]
        with open(file_path, newline='') as csvfile:
            self.__data = list(csv.reader(csvfile, quotechar='|'))[1:]
    
    def boardcast(self):
        for data in self.__data:
            payload = {
                "datetime": data[0],
                "temperature": data[1],
                "humidity": data[2],
                "co2": data[3],
                "id": self.__id
            }
            self.__channel.basic_publish(exchange='pubsub', routing_key='', body=json.dumps(payload))
            time.sleep(self.__time)
        self.close_connection()

    def close_connection(self):
        self.__connection.close()

def run_iqa_sensor(csv_file):
    sensor = IqaSensor()
    sensor.read_csv(csv_file)
    sensor.create_connection(RABBITMQ_HOST)
    sensor.boardcast()

if __name__ == '__main__':
    thread_1 = Process(target=run_iqa_sensor, args=('data/sample_iaq_data_Room101.csv',))
    thread_2 = Process(target=run_iqa_sensor, args=('data/sample_iaq_data_Room102.csv',))
    thread_3 = Process(target=run_iqa_sensor, args=('data/sample_iaq_data_Room103.csv',))

    thread_1.start()
    thread_2.start()
    thread_3.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()

    print("All sensors finished broadcasting")