# HeatControl

Simple script to run on a Raspberry Pi in order to control the temperature in a closed environment. Features a web application to monitor and control the system.

# Components

Features:

* **Raspberry Pi**
  Runs script to reads out sensor data and perform required actions. I'm using a Raspberry Pi 1.
* **Custom Shield**
  A custom shield for the Pi used to connect all components. For more details see the section below.
* **Heater**
  The heater is activated when the temperature drops to low. The heater I applied here is a [300W Heater](https://www.amazon.de/Keramisches-Luftheizelement-Thermostat-PTC-isolierte-elektrische/dp/B07MDCMFCQ/ref=sr_1_1_sspa?keywords=keramisches+luftheizelement&qid=1643123726&sprefix=keramisches+lufthei%2Caps%2C72&sr=8-1-spons&psc=1&smid=A2QDVE2OGM9E0I&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE2NU03NUxQTkpDNjYmZW5jcnlwdGVkSWQ9QTAwNDQ4NTAzTlVOTTRTSFgwSThKJmVuY3J5cHRlZEFkSWQ9QTA0MTY1ODUyV0pQTDlTN1JSTlZKJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==).
* **Fan**
  Provides air circulation to distribute the heat. I'm using a 24V casing fan.
* **Temperature Sensors**
  Used to sense the environment temparature. I'm using two [DS18B20](https://www.amazon.de/AZDelivery-digitaler-Temperatursensor-Temperaturf%C3%BChler-wasserdicht/dp/B07KNQJ3D7/ref=sr_1_1_sspa?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2U0ZHPSJCCDZD&keywords=DS18B20&qid=1643123820&sprefix=ds18b20%2Caps%2C78&sr=8-1-spons&psc=1&smid=A1X7QLRQH87QA3&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExNDlRUkUyWU9RNUZYJmVuY3J5cHRlZElkPUEwODYwNjA4OFhCTVM5VTdLSTUmZW5jcnlwdGVkQWRJZD1BMDYyODIzMDJUOEJXR0dNRUsyV1Imd2lkZ2V0TmFtZT1zcF9hdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl5) temperature sensors in this project and calculate temperature by deriving the mean value of both sensors.

## Custom Shield
![The final Shield](https://drive.google.com/uc?export=view&id=1OCSn7e3RbvjosjuQAcoru9IjI-qDHAVo)
The final soldered shield.

TODO
The shield's circuit.
