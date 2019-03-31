Solight - Homie (MQTT) bridge
=============================

A simple bridge that exposes supported Solight sockets as Homie nodes.

About
-----

This program allows you to use Solight DY01, DY05, and DY08 sockets via MQTT protocol using Homie convention.
It works with OpenHAB.

Dependencies
------------

```
sudo apt-get install pigpio
sudo pip3 install solight-dy01 solight-dy05 solight-dy08
```

Usage
-----

Download this code

```
git clone https://github.com/Kixunil/solight-homie
```

Edit config file according to your needs. Example:

```
{
	"mqtt" : {
		"HOST": "localhost",
		"PORT": 1883,
		"KEEPALIVE": 10,
		"DEVICE_ID": "solight",
		"DEVICE_NAME": "Solight sockets",
		"TOPIC": "homie"
	},
	"transmitter_pin": 17,
	"DY01_sockets": {
		"Table lamp" : 42,
		"Fan livingroom": 43
	},
	"DY05_sockets": {
		"Humidifier": 1,
		"Coffee machine": 2
	},
	"DY08_sockets": {
		"Heater": 1,
		"Speakers": 2,
		"TV": 3
	}
}
```

```
sudo pigpiod
python3 solightd.py
```

The numbers are the addresses of the sockets. The sockets will be exposed on MQTT under given names.
