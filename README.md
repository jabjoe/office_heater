Introduction
------------

This was just a quick project so we could remotely turn on a heater in the office before we got in.
We have some w1 temperature sensors to see if it's working and how cold it is.
The heater is connected to a plug controled by a Energenie.

We use it with a fork of Energenie code:

https://github.com/jabjoe/python-energenie

This means during boot we call the included script "sockinit.sh".



MQTT messages
-------------

office/pi_heater/state         # Is the heater on? 

office/pi_heater/request_state # Turn heater on/off


Temperature sensors will each make a MQTT message.

office/pi_heater/temp_sense0  # First temperature sensor

office/pi_heater/temp_sense1  # Second temperature sensor

office/pi_heater/temp_sense2  # Third temperature sensor 



Running Test
------------

It is called with the arguments:

    <ssl host> <port> <username> <password>

The SSL host with the broker, which obviously must be SSL.

The port will normally 8883 as it's a SSL broker.

The username and password explain themselves.
