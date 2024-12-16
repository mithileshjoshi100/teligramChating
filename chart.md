```mermaid
classDiagram
    class ESP32 {
        - ssid
        - password
        - authToken
        + readDHT22()
        + startServer()
        + sendToBlynk()
    }

    class DHT22 {
        - temperature
        - humidity
        + readData()
    }

    DHT22 --> ESP32 : readData()
