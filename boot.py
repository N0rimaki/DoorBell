# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
import socket
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()



def connect_wifi():
	import network
	ap_if = network.WLAN(network.AP_IF)
	ap_if.active(False)
	
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print("Connect to Nework")
		sta_if.active(True)
		sta_if.connect('IoT_2.4','ForkknifE')
		while not sta_if.isconnected():
			pass
	else:
		print("already connected")
	
	sta_if.ifconfig(('192.168.1.187','255.255.255.0','192.168.1.1','192.168.1.10'))
	print("config: ",sta_if.ifconfig())

connect_wifi()

def sendBootSMS(TexttoSend):
	TCP_IP="192.168.1.39"
	TCP_PORT=54321


	BUFFER_SIZE = 1024
	
	MESSAGE_PDU = 'AT+CMGF=1\r\n'
	MESSAGE_PDU_CHECK = 'AT+CMGF?\r\n'


	recipent = 'AT+CMGS="+43xxxx"\r\n'

	
	MESSAGE_builder = TexttoSend+'\r\n'


	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))
		
		s.send(MESSAGE_PDU.encode())
		data = s.recv(BUFFER_SIZE)
		print ("set PDU:", data)
		
		# s.send(MESSAGE_PDU_CHECK.encode())
		# data = s.recv(BUFFER_SIZE)
		# print ("PDU is:", data)
		
		s.send(recipent.encode())
		data = s.recv(BUFFER_SIZE)
		print ("Recipent result: ", data)
		
		s.send(MESSAGE_builder.encode())
		data = s.recv(BUFFER_SIZE)
		print ("text result:", data)		
		
		s.send(b'\x1a')
		data = s.recv(BUFFER_SIZE)
		print ("result:", data)

	except socket.error as ERR:
		print (ERR)
	finally:
		s.close()
	
	

sendBootSMS("boot.py Rebooted DoorBell")