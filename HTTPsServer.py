try:
	import usocket as socket
except:
	import socket 
#import machine
from	machine	import	ADC
from machine import Pin
import utime


LED = Pin(2, Pin.OUT)
RELAY = Pin(5, Pin.OUT)
ADC0 = ADC(0)
VOLTAGE = ADC0.read()


def blink():
	LED.on()
	utime.sleep_ms(500)
	LED.off()
	utime.sleep_ms(500)

	# RELAY.on()
	# utime.sleep_ms(500)
	# RELAY.off()
	# utime.sleep_ms(500)



#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head> <title>ESP8266 LED ON/OFF</title> </head>
<center><h2>A simple webserver with Micropython</h2></center>
<center><h2>Voltage</h2></center>
<center><h2>%s</h2></center>
<form>
LED: 
<button name="LED" value="ON" type="submit">LED ON</button>
<button name="LED" value="OFF" type="submit">LED OFF</button><br><br>
RELAY: 
<button name="RELAY" value="ON" type="submit">LED ON</button>
<button name="RELAY" value="OFF" type="submit">LED OFF</button>
</form>
</html>
"""

# i = 0
# LED.on()
# #while i < 10:
# while i < 1000:
# 	i += 1
# 	LED.off()
# 	#blink()
# LED.on()

	


#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.bind(('', 80))
s.listen(5)
while True:
	utime.sleep_ms(500)
	VOLTAGE = ADC0.read()
	if VOLTAGE > 512:
		LED.off()
		RELAY.on()
	elif VOLTAGE < 513:
		LED.on()
		RELAY.off()
	# i = 0	
	# while i < 1000:
	# 	i += 1
	try:
		conn, addr = s.accept()
		print("Got a connection from %s" % str(addr))
		request = conn.recv(1024)
		print("Content = %s" % str(request))
		request = str(request)
		LEDON = request.find('/?LED=ON')
		LEDOFF = request.find('/?LED=OFF')
		RELAYON = request.find('/?RELAY=ON')
		RELAYOFF = request.find('/?RELAY=OFF')
		print("Data: " + str(LEDON))
		print("Data2: " + str(LEDOFF))
		VOLTAGE = ADC0.read()
		# if VOLTAGE > 512 and not LEDON == 6 and not LEDOFF == 6 and not RELAYON == 6 and not RELAYOFF == 6:
		# 	LED.off()
		# 	RELAY.on()
		# elif VOLTAGE < 513:
		# 	LED.on()
		# 	RELAY.off()

		if LEDON == 6:
			LED.off()
		elif LEDOFF == 6:
			LED.on()
		elif RELAYON == 6:
			RELAY.on()
		elif RELAYOFF == 6:
			RELAY.off()	

		response = html % VOLTAGE
		conn.send(response)
		conn.close()
	except:
		pass