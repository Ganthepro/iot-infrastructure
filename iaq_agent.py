import pika
from pika.exchange_type import ExchangeType
import time
import csv
import json

class IqaAgent():
    def __init__(self):
        self.__connection = None
        self.__channel = None
        self.__time = 5
        self.__data = []

    def create_connection(self, host: str) -> None:
        connection_parameters = pika.ConnectionParameters(host)
        self.__connection = pika.BlockingConnection(connection_parameters)
        self.__channel = self.__connection.channel()  
        self.__channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

    def read_csv(self, file_path: str):
        with open(file_path, newline='') as csvfile:
            self.__data = list(csv.reader(csvfile, quotechar='|'))[1:]
    
    def boardcast(self):
        for data in self.__data:
            payload = {
                "datetime": data[0],
                "temperature": data[1],
                "humidity": data[2],
                "co2": data[3]
            }
            self.__channel.basic_publish(exchange='pubsub', routing_key='', body=json.dumps(payload))
            print(f"sent data: {data}")
            time.sleep(self.__time)
        self.close_connection()

    def close_connection(self):
        self.__connection.close()

if __name__ == '__main__':
    iqa_agent = IqaAgent()
    iqa_agent.read_csv('data/sample_iaq_data_Room101.csv')
    iqa_agent.create_connection('localhost')
    iqa_agent.boardcast()