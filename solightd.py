import homie
import json
import pigpio
import time
import logging
from dy01 import DY01
from dy05 import DY05
from dy08 import DY08

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

with open("solight_config.json") as config_file:
    config = json.load(config_file)

pi = pigpio.pi()
dy01 = DY01(pi, config["transmitter_pin"])
dy05 = DY05(pi, config["transmitter_pin"], 0.5)
dy08 = DY08(pi, config["transmitter_pin"])

communicator = homie.Device(config["homie"])
communicator.setFirmware("SolightSockets", "1.0.0")
id_counter = 0

def newNodeId():
    global id_counter
    nodeId = "socket%d" % id_counter
    id_counter += 1
    return nodeId

def create_dy01_handler(name, sock):
    def handle_command(property, payload):
        logger.debug("Received message: '%s' for %s" % (payload, name))
        if payload == "true":
            dy01.send(sock, 1)
            property.update("true")
        else:
            dy01.send(sock, 0)
            property.update("false")

    return handle_command

def create_dy05_handler(name, sock):
    def handle_command(property, payload):
        logger.debug("Received message: '%s' for %s" % (payload, name))
        if payload == "true":
            logger.debug("'%s' == 'true'")
            dy05.send(sock, 1, 1)
            property.update("true")
        else:
            logger.debug("'%s' != 'true'")
            dy05.send(sock, 1, 0)
            property.update("false")

    return handle_command

if "DY01_sockets" in config:
    for name, sock in config["DY01_sockets"].iteritems():
        switch = communicator.addNode(newNodeId(), name, "switch")

        on = switch.addProperty("on", name, None, "boolean", None, True)
        on.settable(create_dy01_handler(name, sock))
        on.update("false")

if "DY05_sockets" in config:
    for name, sock in config["DY05_sockets"].iteritems():
        switch = communicator.addNode(newNodeId(), name, "switch")

        on = switch.addProperty("on", name, None, "boolean", None, True)
        on.settable(create_dy05_handler(name, sock))
        on.update("false")

if "DY08_sockets" in config:
    for name, sock in config["DY08_sockets"].iteritems():
        switch = communicator.addNode(newNodeId(), name, "switch")
        def handle_command(property, payload):
            logger.debug("Received message: '%s' for %s" % (payload, name))
            if payload == "true":
                dy08.send(sock, 1)
                property.update("true")
            else:
                dy08.send(sock, 0)
                property.update("false")

        on = switch.addProperty("on", name, None, "boolean", None, True)
        on.settable(create_dy08_handler(name, sock))
        on.update("false")

communicator.setup()

# Yes, this is horrible. Unfortunately, the API doesn't provide
# a better way of blocking.
while True:
    time.sleep(1)
