import pika
from pika.exchange_type import ExchangeType
import time
import csv
import json
from dotenv import load_dotenv
import os

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

if __name__ == '__main__':
    iqa_sensor_1 = IqaSensor()
    iqa_sensor_1.read_csv('data/sample_iaq_data_Room101.csv')
    iqa_sensor_1.create_connection(RABBITMQ_HOST)
    iqa_sensor_1.boardcast()
    
    iqa_sensor_2 = IqaSensor()
    iqa_sensor_2.read_csv('data/sample_iaq_data_Room102.csv')
    iqa_sensor_2.create_connection(RABBITMQ_HOST)
    iqa_sensor_2.boardcast()
    
    iqa_sensor_3 = IqaSensor()
    iqa_sensor_3.read_csv('data/sample_iaq_data_Room103.csv')
    iqa_sensor_3.create_connection(RABBITMQ_HOST)
    iqa_sensor_3.boardcast()