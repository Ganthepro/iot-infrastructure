# IoT Infrastructure

## Clone Git Repository

```bash
git clone https://github.com/Ganthepro/iot-infrastructure.git
```

## Development Setup

- **Prerequisite**
    - PostgreSQL
        
        [PostgreSQL: Downloads](https://www.postgresql.org/download/)
        
    - RabbitMQ
        
        [Installing RabbitMQ | RabbitMQ](https://www.rabbitmq.com/docs/download#installation-guides)
        
1. Install dependency, run this following command
    
    ```bash
    pip install -r requirements.txt
    ```

2. Set up the `.env` file using `.env.example` as a reference
    
    ```bash
    DB_USERNAME=postgres
    DB_PASSWORD=P@ssw0rd!
    DB_HOST=localhost
    DB_DATABASE=postgres
    RABBITMQ_HOST=localhost
    ```
    
3. Run `main.py` from the `data_logger` folder
    
    ```bash
    cd data_logger
    python main.py
    ```
    
4. Run `main.py` from the `iaq_sensor` folder
    
    ```bash
    cd iaq_sensor
    python main.py
    ```
    
5. Navigate to the `api` folder, run this following command
    
    ```bash
    cd api 
    fastapi dev
    ```
    


## Production Setup (Docker Compose)

- **Prerequisite: Docker Engine**
    
    [Install](https://docs.docker.com/engine/install/)
    
1. Set up the `.env` file using `.env.example` as a reference
    
    ```bash
    DB_USERNAME=postgres
    DB_PASSWORD=P@ssw0rd!
    DB_HOST=postgres
    DB_DATABASE=postgres
    RABBITMQ_HOST=rabbitmq
    ```
    
2. Run Docker Compose script, using this following command
    
    ```bash
    docker compose up -d --build
    ```
    


## API Swagger

Open the API Swagger documentation in your browser by navigating to [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) or [`http://localhost:8000/docs`](http://localhost:8000/docs)

![{E832DC68-7F1D-4D23-8CE9-7247678B157A}](https://github.com/user-attachments/assets/99e140af-7ed9-4a4c-b742-36970f7692f9)
Use the API Swagger documentation to query sensor data from the database and delete all data.
