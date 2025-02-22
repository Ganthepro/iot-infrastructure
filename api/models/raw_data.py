from sqlalchemy import Column, Integer, String, TIMESTAMP, UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(String())    
    timestamp = Column(Integer(), nullable=False)
    datetime = Column(TIMESTAMP, nullable=False)
    datapoint = Column(String(), nullable=False)
    value = Column(String(), nullable=False)