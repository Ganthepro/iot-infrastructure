import pika
from pika.exchange_type import ExchangeType
import json
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
from datetime import datetime as dt
import pytz
from dotenv import load_dotenv
import os
import uuid

load_dotenv(override=True)

DATABASE = os.getenv("DB_DATABASE")
PASSWORD = os.getenv("DB_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
DB_HOST = os.getenv("DB_HOST")

url = URL.create(
    drivername="postgresql",
    username="postgres",
    host=DB_HOST,
    database=DATABASE,
    password=PASSWORD
)
engine = create_engine(url)

class DataLogger:
    def __init__(self, session):
        self.__connection = None
        self.__channel = None
        self.__queue = None
        self.__session = session

    def create_connection(self, host: str) -> None:
        connection_parameters = pika.ConnectionParameters(host)
        self.__connection = pika.BlockingConnection(connection_parameters)
        self.__channel = self.__connection.channel()  
        self.__channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)
        self.__queue = self.__channel.queue_declare(queue='', exclusive=True)
        self.__channel.queue_bind(exchange='pubsub', queue=self.__queue.method.queue)

    def receive(self):
        self.__channel.basic_consume(queue=self.__queue.method.queue, auto_ack=True,
        on_message_callback=self.__on_message_received)
        self.__channel.start_consuming()

    def __on_message_received(self, ch, method, properties, body):
        body = json.loads(body)
        self.insert(body)

    def insert(self, body):
        datetime_str = body['datetime']
        date_time = dt.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
        timestamp = int(date_time.replace(tzinfo=pytz.UTC).timestamp())
        datetime_timestamptz = date_time.replace(tzinfo=pytz.UTC)

        temperature = RawData(
            device_id=body["id"],
            timestamp=timestamp,
            datetime=datetime_timestamptz,
            datapoint="temperature",
            value=body["temperature"]
        )
        humidity = RawData(
            device_id=body["id"],
            timestamp=timestamp,
            datetime=datetime_timestamptz,
            datapoint="humidity",
            value=body["humidity"]
        )
        co2 = RawData(
            device_id=body["id"],
            timestamp=timestamp,
            datetime=datetime_timestamptz,
            datapoint="co2",
            value=body["co2"]
        )
        self.__session.add(temperature)
        self.__session.add(humidity)
        self.__session.add(co2)
        self.__session.commit()

Base = declarative_base()

class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String())    
    timestamp = Column(Integer(), nullable=False)
    datetime = Column(TIMESTAMP, nullable=False)
    datapoint = Column(String(), nullable=False)
    value = Column(String(), nullable=False)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    data_logger = DataLogger(session)
    data_logger.create_connection(RABBITMQ_HOST)
    data_logger.receive()