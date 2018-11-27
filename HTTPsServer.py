try:
	import usocket as socket
except:
	import socket 
import machine
import utime


LED = machine.Pin(2, machine.Pin.OUT)
RELAY = machine.Pin(5, machine.Pin.OUT)


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

# while True:
# 	blink()


#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
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
	if LEDON == 6:
		LED.off()
	if LEDOFF == 6:
		LED.on()
	if RELAYON == 6:
		RELAY.on()
	if RELAYOFF == 6:
		RELAY.off()
	response = html
	conn.send(response)
	conn.close()