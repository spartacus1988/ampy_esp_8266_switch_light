try:
	import usocket as socket
except:
	import socket 
import machine
import utime

LED = machine.Pin(2, machine.Pin.OUT)
RELAY = machine.Pin(5, machine.Pin.OUT)
ADC0 = machine.ADC(0)
VOLTAGE = ADC0.read()
REQUEST_WAS_RECEIVED = False

def blink():
	LED.on()
	utime.sleep_ms(500)
	LED.off()
	utime.sleep_ms(500)


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
<button name="RELAY" value="ON" type="submit">RELAY ON</button>
<button name="RELAY" value="OFF" type="submit">RELAY OFF</button><br><br>
RESET BUTTON:
<button name="RESET" value="ON" type="submit">HARD RESET</button>
</form>
</html>
"""


#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.bind(('', 80))
s.listen(5)
while True:
	utime.sleep_ms(500)
	VOLTAGE = ADC0.read()
	if not REQUEST_WAS_RECEIVED:
		if VOLTAGE > 512:
			LED.off()
			RELAY.on()
		elif VOLTAGE < 513:
			LED.on()
			RELAY.off()
	# i = 0	
	# while i < 1000:
	# 	i += 1
	while True:
		try:
			conn, addr = s.accept()
			REQUEST_WAS_RECEIVED = True
			print("Got a connection from %s" % str(addr))
			request = conn.recv(1024)
			print("Content = %s" % str(request))
			request = str(request)
			LEDON = request.find('/?LED=ON')
			LEDOFF = request.find('/?LED=OFF')
			RELAYON = request.find('/?RELAY=ON')
			RELAYOFF = request.find('/?RELAY=OFF')
			RESET = request.find('/?RESET=ON')
			print("Data: " + str(LEDON))
			print("Data2: " + str(LEDOFF))
			VOLTAGE = ADC0.read()

			if LEDON == 6:
				LED.off()
			elif LEDOFF == 6:
				LED.on()
			elif RELAYON == 6:
				RELAY.on()
			elif RELAYOFF == 6:
				RELAY.off()
			elif RESET == 6:
				machine.reset()

			response = html % VOLTAGE
			conn.send(response)
			conn.close()
		except:
			break