```mermaid
classDiagram
    class ESP32 {
        - ssid
        - password
        - authToken
        - dbConnection
        - cloudConfig
        + readDHT22()
        + startServer()
        + sendToBlynk()
        + storeToDB()
        + sendToCloud()
        + runMLModel()
    }

    class DHT22 {
        - temperature
        - humidity
        + readData()
    }

    class CloudService {
        - dataStorage
        - mlModels
        - globalAccess
        + processData()
        + generateReport()
        + enhanceAccess()
    }

    DHT22 --> ESP32 : readData()
    ESP32 --> CloudService : sendToCloud(), storeToDB()
    ESP32 --> CloudService : runMLModel()
    CloudService --> ESP32 : generateReport(), enhanceAccess()
