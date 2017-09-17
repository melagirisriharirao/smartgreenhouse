"""
This is the code that needs to be running in Raspberry Pi.
"""

import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT
import datetime
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import smtplib

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setwarnings(False)

#fan pin 29
#lights pin 31
#cover pin 35
#valve pin 32

global temp_thresh_new
temp_thresh_new=27
global lbreak
lbreak=1
global humid_thresh_new
humid_thresh_new = 500
global light_thresh_new
light_thresh_new = 500
global lights
lights="off"
global valve
valve="off"
global cover
cover="closed"
global fan
fan="off"
global flag
flag = True
global mail_count
mail_count = 0

global tem
tem = 25
global hum
hum = 60

GPIO.output(29, False)
GPIO.output(31, False)
GPIO.output(33, False)
GPIO.output(35, False)
GPIO.output(37, False)
GPIO.output(32, False)
GPIO.output(36, False)

loc = "/home/pi/Desktop"

fname = "pi_action_log.txt"

floc = os.path.join(loc,fname)

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

class Sensor_val():
	def read_val(self):
		# Read all the ADC channel values in a list.
		val = [0]*8
		for i in range(8):
		    # The read_adc function will get the value of the specified channel (0-7).
		    val[i] = mcp.read_adc(i)
		humidity, temperature = Adafruit_DHT.read_retry(11, 27)


		if temperature < 20:
			global tem
			temperature = tem
		if humidity > 100:
			global hum
			humidity = hum

		values = {'Soil': val[0], 'Lum': val[1], 'Rain': val[2], 'Soil1': val[3], 'Temp': temperature, 'Humid': humidity}

		global tem
		global hum

		tem = temperature
		hum = humidity

		return values

class Device_state():
	def read_state(self):
		
		global fan
		global cover 
		global valve
		global lights

		state = {'Cover': cover,'Light': lights,'Fan': fan,'Valve': valve}
		print state
		return(state)

class Auto_mode():
	def automatic(self):
		timevar = datetime.datetime.now()

		date = str(timevar.day) + "-" + str(timevar.month) + "-" + str(timevar.year)  

		now = str(timevar.strftime("%H")) + ":" + str(timevar.strftime("%M")) + ":" + str(timevar.strftime("%S")) 

		if timevar.hour%2 == 0:
			global mail_count
			mail_count = mail_count+1
			if mail_count == 1:
				fromaddr = "havishwas@gmail.com"
				toaddr = "havishwas@gmail.com"
				msg = MIMEMultipart()

				msg['Subject'] = "GREEN HOUSE UPDATE"
				body = " "
				msg.attach(MIMEText(body, 'plain'))
	 
				filename = "pi_action_log.txt"
				attachment = open("/home/pi/Desktop/pi_action_log.txt", "rb")
				part = MIMEBase('application', 'octet-stream')
				part.set_payload((attachment).read())
				encoders.encode_base64(part)
				part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
				msg.attach(part)
				server = smtplib.SMTP('smtp.gmail.com', 587)
				server.starttls()
				server.login(fromaddr, "Vishwas123$")
				text = msg.as_string()
				server.sendmail(fromaddr, toaddr, text)
				server.quit()
				os.remove("/home/pi/Desktop/pi_action_log.txt")
				loc = "/home/pi/Desktop/"
				fname = "pi_action_log.txt"
				with open(fname,'w+') as f:
					readfile = f.read()
					name = f.name
					f.write("DATE    " + "	TIME    " + "	TEMP "+ "	HUMID"+ "	MOIST" +"	LUM" +"	RAIN"+"	ACTION TAKEN\n" )
					f.close()
					
		else:
			global mail_count
			mail_count=0
			
		loc = "/home/pi/Desktop"

		fname = "pi_action_log.txt"

		val = Sensor_val()
		value = val.read_val()
		timevar = datetime.datetime.now()
		print("auto mode started :) ")
		print(value)

		global temp_thresh_new
		#temp_thresh_new=27
		global humid_thresh_new
		#humid_thresh_new = 50
		global light_thresh_new
		#light_thresh_new = 500

		global fan
		global cover 
		global valve
		global lights


		if ((value['Rain'] < 600) or (value['Temp'] > temp_thresh_new) or (value['Humid'] > humid_thresh_new) or (value['Soil'] < 500)):
			#GPIO.output(35, True) #cover
			global cover
			if cover == "closed":
				pass
			else:
				print("COVER CLOSED")
				GPIO.output(35, False)
				GPIO.output(36, True)
				time.sleep(10)
				GPIO.output(35, False)
				GPIO.output(36, False)
				global cover
				cover = "closed"
			#print("roof "+ roof+"  windows " +windows +"  fan "+fan)
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Cover closed"))			
				f.close()

		else:
#			GPIO.output(35, False)
			global cover
			if cover == "opened":
				pass
			else:
				print("COVER OPENED")
				cover = "opened"
				GPIO.output(35, True)
				GPIO.output(36, False)
				time.sleep(10)
				GPIO.output(35, False)
				GPIO.output(36, False)
			#print("roof "+ roof+"  windows " +windows +"  fan "+fan)
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Cover opened"))
				f.close()

		if (((value['Temp'] > temp_thresh_new) or (value['Humid'] > humid_thresh_new))):#and ((time.minute % 5) == 0)):
			GPIO.output(29, True) #fan
			global fan
			fan = "on"
			print("cover "+ cover+"  fan "+fan +"  threshhold" +str(temp_thresh_new))
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Fan ON"))
				f.close()
		else:
			GPIO.output(29, False)
			global fan
			fan = "off"
		#	print("roof "+ roof+"  windows " +windows +"  fan "+fan)
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Fan OFF"))
				f.close()

		if ((value['Soil']>900)):
			GPIO.output(32, True) #valve
			global valve
			valve = "on"
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Valve ON"))
				f.close()
		else:
			GPIO.output(32, False) #valve
			global valve
			valve = "off"
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Valve OFF"))
				f.close()

		if value['Lum'] > light_thresh_new:
			GPIO.output(31, True) #lights
			global lights
			lights = "on"
		#	print("lights " + lights)
			#time.sleep(3)
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Lights ON"))
				f.close()
		else:
			GPIO.output(31, False)
			global lights
			lights = "off"
		#	print("lights " + lights)
			with open(floc,'a+') as f:
				readfile = f.read()
				name = f.name
				f.write("{}	{}	{}	{}	{}	{}	{}	{} \n".format(date, now, value['Temp'], value['Humid'], value['Soil'], value['Lum'], value['Rain'], "Lights OFF"))
				f.close()

		val = Device_state()
		state = val.read_state()
		return

class Man_mode():
	def manual(self):
		flag = 1
		while True:
			global flag
			#print("finished autochk..")
			print("entered manual mode..")

			def on_connect(client, userdata, flags, rc):
				print("Connected with usercode" + str(rc))
				mqttc.subscribe("/hari")
			def on_message(client, userdata, msg):
				print(msg.topic)
				message = (msg.payload).decode()
				print(message)

				global fan
				global cover 
				global valve
				global lights

				if message == "measurements":
					val = Sensor_val()
					value = val.read_val()
					value = str(value)
					print(value)
					mqttc.publish("/hp", value, 1)

				if message == "state":
					val = Device_state()
					state = val.read_state()
					state = str(state)
					print(state)
					mqttc.publish("/hp", state, 1)

				if message == "autoMode":
					global flag
					flag = True
					print("Flag set to true")
					print("switching to auto")
					autoobj = Auto_mode()
					auto = autoobj.automatic()
					#mqttc.loop_stop()
				
				if message =="lightsOn":
					global lights
					GPIO.output(31, True)
					print("TURNED ON")
					lights = "on"

				if message == "lightsOff":
					global lights
					GPIO.output(31, False)
					print("TURNED OFF")
					lights = "off"

				if message == "coverClose":
					global cover
					if cover == "closed":
						pass
					else:
						print("COVER CLOSED")
						cover = "closed"
						GPIO.output(35, False)
						GPIO.output(36, True)
						time.sleep(10)
						GPIO.output(35, False)
						GPIO.output(36, False)
				

				if message == "coverOpen":
					global cover
					if cover == "opened":
						pass
					else:
						print("COVER OPENED")
						GPIO.output(35, True)
						GPIO.output(36, False)
						cover = "opened"
						time.sleep(10)
						GPIO.output(35, False)
						GPIO.output(36, False)

				if message =="valveOn":
					global valve
					print("VALVE ON")
					GPIO.output(32, True)
					valve = "on"

				if message == "valveOff":
					global valve
					print("VALVE OFF")
					GPIO.output(32, False)
					valve = "off"

				if message == "fanOn":
					global fan
					print("FAN ON")
					GPIO.output(29,True)
					fan="on"

				if message == "fanOff":
					global fan
					print("FAN OFF")
					GPIO.output(29,False)
					fan="off"
				
				if message == "marieGold":
					global temp_thresh_new
					temp_thresh_new = 30
					global humid_thresh_new
					humid_thresh_new = 50
					global light_thresh_new
					light_thresh_new = 500
					print("Marie Gold crop settings applied")

				if message == "rose":
					global temp_thresh_new
					temp_thresh_new = 24
					global humid_thresh_new
					humid_thresh_new = 50
					global light_thresh_new
					light_thresh_new = 500
					print("Rose crop settings applied")


				if message == "manMode":
					global flag
					flag = False
					print("Flag set to false")

			if flag == True:
				autoobj = Auto_mode()
				auto = autoobj.automatic()

			mqttc = mqtt.Client()
			
			mqttc.on_connect = on_connect
			mqttc.on_message = on_message
			mqttc.connect("broker.hivemq.com", 1883, 60)
			
			time.sleep(20)
			
			mqttc.loop_start()

while True:
	manobj = Man_mode()
	man = manobj.manual()
