from azure.iot.device import IoTHubDeviceClient
import time

# Replace with your IoT Edge device connection string
CONNECTION_STRING = "HostName=cloud-to-device.azure-devices.net;DeviceId=building-a;ModuleId=iaq-sensor-agent;SharedAccessKey=g+Ge+9i94PSJWCnsqPfqdAVCHhAaIboWrxUQs/CjXXA="

def main():
    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        client.connect()
        print("Connected to IoT Hub!")

        # Send a test message
        message = "Hello from IoT Edge!"
        client.send_message(message)
        print("Message sent!")
        time.sleep(300)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("Disconnected from IoT Hub.")

if __name__ == "__main__":
    main()
