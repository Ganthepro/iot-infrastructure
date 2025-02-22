from fastapi import FastAPI, Depends
from database import engine, get_db
from models.raw_data import Base, RawData
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/data")
def read_all_data(db: Session = Depends(get_db)):
    return db.query(RawData).all()

@app.delete("/data")
def delete_all_data(db: Session = Depends(get_db)):
    db.query(RawData).delete()
    db.commit()
    return {"message": "All data deleted successfully"}