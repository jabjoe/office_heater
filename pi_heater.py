#! /usr/bin/python3

import os
import sys
import time
import paho.mqtt.client as paho
import energenie



current_state = "office/pi_heater/state"
next_state    = "office/pi_heater/request_state"

sensor_temp_base = "office/pi_heater/temp_sense"


class pi_heater_t:
    def __init__(self, hostname, port, username, password):
        self.client = paho.Client("pi-heater-control")
        self.client.tls_set()
        self.client.username_pw_set(username, password)
        self.hostname = hostname
        self.port = port
        self._connected = False
        self._connect()

        self.state = False
        self.sensors = []

        for f in os.listdir("/sys/bus/w1/devices/"):
            if f.find("bus_master") == -1:
                self.sensors += [ os.path.join("/sys/bus/w1/devices/", f) ]

    def _connect(self):
        try:
            self.client.connect(self.hostname, self.port)
            self.client.on_message = lambda c, u, m : self._on_message(u, m)

            self.client.publish(current_state, "off")
            self.client.subscribe(next_state)
            self.client.on_disconnect = lambda client, userdata, rc : self._connect()
            self._connected = True
            print("Connected")
        except Exception as e:
            print("Failed to connect : %s" % str(e))
            self._connected = False


    def _read_sensor(self, sensor):
        try:
            with open(os.path.join(sensor, "w1_slave")) as f:
                line = f.readline()
                crc = line.rsplit(' ',1)
                crc = crc[1].replace('\n', '')
                if crc=='YES':
                    line = f.readline()
                    raw = line.rsplit('t=',1)[1].strip()
                    temp = int(raw) / 1000.0
                    #print(sensor, ":", temp, "degrees")
                    return temp
                else:
                    print(sensor, "CRC failed")
                    return None
        except Exception as e:
            print("Failed to read", sensor, str(e))
            return None


    def _update_others(self):
        self.client.publish(current_state, "on" if self.state else "off")
        for n in range(0, len(self.sensors)):
            temp = self._read_sensor(self.sensors[n])
            if temp is not None:
                self.client.publish(sensor_temp_base + str(n), temp)

    def _on_message(self, userdata, message):

        print(message.topic, "=", message.payload)

        if message.topic == next_state:
            if message.payload == b"on":
                energenie.switch_on(1)
                self.state = True
                self._update_others()
            elif message.payload == b"off":
                energenie.switch_off(1)
                self.state = False
                self._update_others()

    def loop(self):
        if self._connected:
            self.client.loop()
            self._update_others()
        else:
            self._connect()

    def finish(self):
        self.client.disconnect()

    def is_running(self):
        return True



def main():

    if len(sys.argv) < 5:
        print("<ssl host> <port> <username> <password>")
        sys.exit(-1)

    if os.getenv("DEBUG"):
        global _debug
        _debug = True

    hostname   = sys.argv[1]
    port       = int(sys.argv[2])
    username   = sys.argv[3]
    password   = sys.argv[4]

    energenie.switch_off()

    pi_heater = pi_heater_t(hostname, port, username, password)

    while pi_heater.is_running():
        pi_heater.loop()
        time.sleep(1)


    pi_heater.finish()



if __name__ == "__main__":
    main()



