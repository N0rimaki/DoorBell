import socket
import machine
adc = machine.ADC(0)

# http://micropython.org/webrepl/?#192.168.1.187:8266/

#################################

#https://maker.pro/esp8266/tutorial/how-to-program-an-esp8266-with-micropython
#https://github.com/espressif/esptool
#http://micropython.org/download/esp8266/

#https://forum.iobroker.net/topic/7660/siedle-klingel-t%C3%BCr%C3%B6ffner-mit-esp8266-und-mqtt/17
#https://www.panbachi.de/smarte-tuerklingel-alte-sprechanlage-smart-machen/


#https://docs.micropython.org/en/latest/esp8266/tutorial/adc.html
#https://ep.advantech-bb.cz/support/router-models/download/340/at-commands-application-note-20190424.pdf	





def sendsmsocket(TextToSend):
	TCP_IP="192.168.1.39"
	TCP_PORT=54321


	BUFFER_SIZE = 1024
	
	MESSAGE_PDU = 'AT+CMGF=1\r\n'
	MESSAGE_PDU_CHECK = 'AT+CMGF?\r\n'


	numbers= ("+43xxxx","+43xxxx")
	customtexts =("FBI, open up!","Schweißgebadet steh i vor ira Dia!","Es schellet gar sehr!","Die Jehovas san do!")

	
	MESSAGE_builder = TextToSend+'\r\n'



	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))
		
		s.send(MESSAGE_PDU.encode())
		data = s.recv(BUFFER_SIZE)
		print ("set PDU:", data)
		
		# s.send(MESSAGE_PDU_CHECK.encode())
		# data = s.recv(BUFFER_SIZE)
		# print ("PDU is:", data)
		
		for p in numbers:
			Recipent = 'AT+CMGS="'+p+'"\r\n'
			print ("Recipent: ", Recipent)
			s.send(Recipent.encode())
			data = s.recv(BUFFER_SIZE)
			print ("Recipent result: ", data)
			
			
			s.send(MESSAGE_builder.encode())
			data = s.recv(BUFFER_SIZE)
			print ("text result:", data)		
			
			s.send(b'\x1a')
			data = s.recv(BUFFER_SIZE)
			print ("result: ", data)

	except socket.error as ERR:
		print (ERR)
	finally:
		s.close()
	
	


def loop():
	z= adc.read()
	t=0
	if z>500 and t >= 0:
		print("Ding Dong - "+str(z))
		t=1
		#TODO
		#add customtexts
		sendsmsocket("Ding Dong... Tuerklingel")
	else:
		print("nix- "+str(z))
		t=0
while True:
	loop()