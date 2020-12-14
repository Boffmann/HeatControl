# HeatControl

Simple script to run on a Raspberry Pi in order to control the temperature in a closed environment.

# Components

Features:

* **Raspberry Pi**
	Reads out sensor data and performs required actions. I'm using a Raspberry Pi 1.
* **Custom Shield**
  A custom shield for the Pi used to connect all components. For more details see the section below.
* **Heating Blanket**
  The heating foil is activated when the temperature drops to low in order to heat up the environment. The foil applied here is a [THF-100200](https://www.reichelt.de/heizfolie-24v-20w-100x200-mm-einzeln-thf-100200-p108464.html?&nbc=1)
* **Fan**
  Provides air circulation to distribute the heat. I'm using a 24V casing fan.
* **Temperature Sensors**
  Used to sense the environment temparature. I'm using four [LM35 DZ](https://secure.reichelt.de/temperatursensor-0-100-c-to92-lm-35-dz-p109402.html?search=LM35) temperature sensors in this project.

## Custom Shield
![The final Shield](https://drive.google.com/uc?export=view&id=1OCSn7e3RbvjosjuQAcoru9IjI-qDHAVo)