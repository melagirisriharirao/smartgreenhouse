"""
This is the source code of IOTSGH application that is built using Kivy.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.graphics.context_instructions import Color
from kivy.uix.scrollview import ScrollView
from kivy.graphics.vertex_instructions import(Rectangle,
											  Line,
											  Ellipse)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.base import runTouchApp
from kivy.lang import Builder
import paho.mqtt.client as mqtt
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
import ast

mqttc = mqtt.Client()
mqttc.connect("broker.hivemq.com", 1883, 60)

class WelcomeScreen(Screen):
	pass

class FirstScreen(Screen):
	def fetch_measurements(self, *args):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.subscribe("/hari")
			mqttc.publish("/hari", "measurements", 1)

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def fetch_state(self, *args):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.subscribe("/hari")
			mqttc.publish("/hari", "state", 1)

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

class SecondScreen(Screen):
	def fetch_data(self, *args):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			client.subscribe("/hp")

		def on_message(client, userdata, msg):
			print(msg.topic+" "+ str(msg.payload))
			message = (msg.payload).decode()
			message = ast.literal_eval(message)
			temp = str(message['Temp'])
			label = self.ids["temp_label"]
			label.text = temp
			humid = str(message['Humid'])
			label = self.ids["humid_label"]
			label.text = humid
			soil = str(message['Soil'])
			label = self.ids["soil_label"]
			label.text = soil
			lum = str(message['Lum'])
			label = self.ids["lum_label"]
			label.text = lum
			wind = str(message['Wind'])
			label = self.ids["wind_label"]
			label.text = wind
			rain = str(message['Rain'])
			label = self.ids["rain_label"]
			label.text = rain

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect
		mqttc.on_message = on_message

		mqttc.loop_start()


class ThirdScreen(Screen):
	def fetch_data(self, *args):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			client.subscribe("/hp")

		def on_message(client, userdata, msg):
			print(msg.topic+" "+ str(msg.payload))
			message = (msg.payload).decode()
			message = ast.literal_eval(message)
			 = str(message['Roof'])
			label = self.ids["cover_label"]
			label.text = cover
			light = str(message['Light'])
			label = self.ids["light_label"]
			label.text = light
			pump = str(message['Pump'])
			label = self.ids["pump_label"]
			label.text = pump
			valve = str(message['Valve'])
			label = self.ids["valve_label"]
			label.text = valve
			fan = str(message['Fan'])
			label = self.ids["fan_label"]
			label.text = fan

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect
		mqttc.on_message = on_message

		mqttc.loop_start()

class FourthScreen(Screen):

	def auto_mode(self):
		self.label = self.ids["mode_label"]
		self.label.text = "AUTOMATIC MODE IS ACTIVE"
		self.button = self.ids["manmode_but"]
		self.button.background_color = 0.6, 0.2, 0.15, 1
		self.button = self.ids["automode_but"]
		self.button.background_color = 0.33, 1, 0.20, 0.3

		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'autoMode')

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def man_mode(self):
		self.label = self.ids["mode_label"]
		self.label.text = "MANUAL MODE IS ACTIVE"
		self.button = self.ids["automode_but"]
		self.button.background_color = 0.6, 0.2, 0.15, 1
		self.button = self.ids["manmode_but"]
		self.button.background_color = 0.33, 1, 0.20, 0.3

		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'manMode')

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

class FifthScreen(Screen):

	def cover_open(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'coverOpen')

		label = self.ids["disp_label"]
		label.text = "COVER OPENED"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def cover_close(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'coverClose')

		label = self.ids["disp_label"]
		label.text = "COVER CLOSED"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def lights_on(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'lightsOn')

		label = self.ids["disp_label"]
		label.text = "LIGHTS TURNED ON"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def lights_off(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'lightsOff')

		label = self.ids["disp_label"]
		label.text = "LIGHTS TURNED OFF"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def pump_on(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'pumpOn')

		label = self.ids["disp_label"]
		label.text = "PUMP TURNED ON"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def pump_off(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'pumpOff')

		label = self.ids["disp_label"]
		label.text = "PUMP TURNED OFF"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def valve_on(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'valveOn')

		label = self.ids["disp_label"]
		label.text = "VALVE TURNED ON"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def valve_off(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'valveOff')

		label = self.ids["disp_label"]
		label.text = "VALVE TURNED OFF"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def fan_on(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'fanOn')

		label = self.ids["disp_label"]
		label.text = "FAN TURNED ON"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def fan_off(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", 'fanOff')

		label = self.ids["disp_label"]
		label.text = "FAN TURNED OFF"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()


class SixthScreen(Screen):
	def mariegold(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", "marieGold")

		label = self.ids["disp_label"]
		label.text = "MARIE GOLD CROP SETTINGS APPLIED"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

	def rose(self):
		def on_connect(client, userdata, flags, rc):
			print("Connected with usercode" + str(rc))
			mqttc.publish("/hari", "rose")

		label = self.ids["disp_label"]
		label.text = "ROSE CROP SETTINGS APPLIED"

		mqttc = mqtt.Client()
		mqttc.connect("broker.hivemq.com", 1883, 60)
		mqttc.on_connect = on_connect

		mqttc.loop_start()

class MyScreenManager(ScreenManager):

	def __init__(self,**kwargs):
	    super(MyScreenManager,self).__init__(**kwargs)
	    Window.bind(on_keyboard=self.Android_back_click)


	def Android_back_click(self,window,key,*largs):
		if key == 27:
			if self.current == 'first':
				pop = ExitPopup()
				pop.build()
				return True
			elif self.current == 'fifth':
				self.current = 'fourth'
				return True
			else:
				self.current = 'first'
				return True


class ExitPopup(Screen):
	def build(self):
		content = ConfirmPopup(text='Do you want to exit?')
		content.bind(on_answer=self._on_answer)
		self.popup = Popup(title="Exit App?",
							title_color=(0.33,1,0.20,0.3),
							title_size = '25sp',
							title_align = 'center',
							separator_color = (0.33,1,0.20,0.1),
							content=content,
							size_hint=(None, None),
							size=(800,1000),
							auto_dismiss= False)
		self.popup.open()
	def _on_answer(self, instance, answer):
		if answer == 'yes':
			App.get_running_app().stop()
		else:
			self.popup.dismiss()

class ConfirmPopup(GridLayout):
	text = StringProperty()

	def __init__(self,**kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup,self).__init__(**kwargs)

	def on_answer(self, *args):
		pass



root_widget = Builder.load_string('''

MyScreenManager:
	WelcomeScreen:
	FirstScreen:
	SecondScreen:
	ThirdScreen:
	FourthScreen:
	FifthScreen:
	SixthScreen:
	ExitPopup:

<WelcomeScreen>:
	name: 'welcome'
	BoxLayout:
		orientation: "vertical"
		canvas.before:
			Color:
				rgba: 0.33, 1, 0.20, 0.3
			Rectangle:
				size: self.size
				pos: self.pos
		color: 1, 1, 1, 1
		Label:
			text: "SMART GREEN HOUSE"
			size_hint_y: None
			height: "45dp"
			bold: True
			font_size: "35dp"
		Label:
			text: "UNDER THE GUIDENCE OF"
			size_hint_y: None
			height: "30dp"
		Label:
			text: "ROOPA S"
			size_hint_y: None
			height: "30dp"
			bold: True

		Label:
			text: "By"
			size_hint_y: None
			height: "50dp"
		Label:
			text: "VISHWAS H A"
			size_hint_y: None
			height: "30dp"
		Label:
			text: "YASHWANTH H P"
			size_hint_y: None
			height: "30dp"
		Label:
			text: "SRIHARI RAO M"
			size_hint_y: None
			height: "30dp"
		Label:
			text: "TIPPESWAMI"
			size_hint_y: None
			height: "30dp"
		Button:
			text: "ENTER"
			background_normal: ''
			background_color: 0.33, 1, 0.20, 0.4
			on_release: app.root.current = 'first'
			size_hint_y: None
			height: "50dp"

<FirstScreen>:
	name: 'first'
	BoxLayout:
		orientation: "vertical"
		Label:
			text: "SMART GREEN HOUSE"
			bold: True
			size_hint_y: None
			height: "90dp"
			canvas.before:
				Color:
					rgba: 0.33, 1, 0.20, 0.3
				Rectangle:
					size: self.size
					pos: self.pos
			color: 1, 1, 1, 1
		Button:
			text: "MEASUREMENTS"
			background_normal: ''
			background_color: 0.33, 1, 0.20, 0.4
			on_release: app.root.current = 'second'
			on_press: root.fetch_measurements()
		Button:
			text: "DEVICE STATE"
			background_normal: ''
			background_color: 0.33, 1, 0.20, 0.4
			on_release: app.root.current = 'third'
			on_press: root.fetch_state()
		Button:
			text: "CONTROLS"
			background_normal: ''
			background_color: 0.33, 1, 0.20, 0.4
			on_release: app.root.current = 'fourth'
		Button:
			text: "SETTINGS"
			background_normal: ''
			background_color: 0.33, 1, 0.20, 0.4
			on_release: app.root.current = 'sixth'


<SecondScreen>:
	name: 'second'
	on_enter: root.fetch_data()
	BoxLayout:
		orientation: 'vertical'
		GridLayout:
			rows:6
			cols:2
			canvas:
				Color:
					rgba: 0.33, 1, 0.20, 0.3
				Rectangle:
					size: self.size
					pos: self.pos
			color: 1, 1, 1, 1
			orientation: 'vertical'
			Label:
				text: "TEMPERATURE"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: temp_label
				text: ''
			Label:
				text: "HUMIDITY"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: humid_label
				text: ''
			Label:
				text: "SOIL MOISTURE"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: soil_label
				text: ''
			Label:
				text: "LUMINOSITY"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: lum_label
				text: ''
			Label:
				text: "WIND SPEED"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: wind_label
				text: ''
			Label:
				text: "RAINING"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: rain_label
				text: ''

<ThirdScreen>:
	name: 'third'
	on_enter: root.fetch_data()
	BoxLayout:
		orientation: 'vertical'
		GridLayout:
			rows:6
			cols:2
			canvas:
				Color:
					rgba: 0.33, 1, 0.20, 0.3
				Rectangle:
					size: self.size
					pos: self.pos
			color: 1, 1, 1, 1
			orientation: 'vertical'
			Label:
				text: "ROOF"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: roof_label
				text: ''
			Label:
				text: "WINDOWS"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: windows_label
				text: ''
			Label:
				text: "LIGHT"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: light_label
				text: ''
			Label:
				text: "PUMP"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: pump_label
				text: ''
			Label:
				text: "VALVE"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: valve_label
				text: ''
			Label:
				text: "FAN"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Label:
				id: fan_label
				text: ''

<FourthScreen>:
	name: 'fourth'
	BoxLayout:
		orientation: 'vertical'
		GridLayout:
			rows:3
			cols:1
			canvas:
				Color:
					rgba: 0.33, 1, 0.20, 0.3
				Rectangle:
					size: self.size
					pos: self.pos
			color: 1, 1, 1, 1
			orientation: 'vertical'
			Button:
				id: automode_but
				text: "ACTIVATE AUTOMATIC MODE"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
				on_release: root.auto_mode()
			Button:
				id: manmode_but
				text: "ACTIVATE MANUAL MODE"
				background_normal: ''
				background_color: 0.6, 0.2, 0.15, 1
				on_press: root.man_mode()
				on_release: app.root.current = 'fifth'
		BoxLayout:
			orientation: 'vertical'
			size_hint_y: None
			height: "400dp"
			Label:
				id: mode_label
				text: 'AUTOMATIC MODE IS ACTIVE'
				canvas:
					Color:
						rgba: 0.33, 1, 0.20, 0.3
					Rectangle:
						size: self.size
						pos: self.pos
				color: 1, 1, 1, 1

<FifthScreen>:
	name: 'fifth'
	BoxLayout:
		orientation: 'vertical'
		GridLayout:
			rows:5
			cols:3
			canvas:
				Color:
					rgba: 0.33, 1, 0.20, 0.2
				Rectangle:
					size: self.size
					pos: self.pos
			color: 1, 1, 1, 1
			orientation: 'vertical'
			Label:
				text: "COVER"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Button:
				text: "OPEN"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.cover_open()
			Button:
				text: "CLOSE"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.cover_close()
			Label:
				text: "LIGHT"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Button:
				text: "ON"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.lights_on()
			Button:
				text: "OFF"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.lights_off()
			Label:
				text: "WATER PUMP"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Button:
				text: "ON"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.pump_on()
			Button:
				text: "OFF"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.pump_off()
			Label:
				text: "VALVE"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Button:
				text: "ON"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.valve_on()
			Button:
				text: "OFF"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.valve_off()
			Label:
				text: "FAN"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
			Button:
				text: "ON"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.fan_on()
			Button:
				text: "OFF"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.2
				on_release: root.fan_off()
		BoxLayout:
			orientation: 'vertical'
			size_hint_y: None
			height: "80dp"
			Label:
				id: disp_label
				text: ''
				canvas:
					Color:
						rgba: 0.33, 1, 0.20, 0.3
					Rectangle:
						size: self.size
						pos: self.pos
				color: 1, 1, 1, 1

<SixthScreen>:
	name: 'sixth'
	BoxLayout:
		orientation: 'vertical'
		GridLayout:
			rows:2
			cols:1
			canvas:
				Color:
					rgba: 0.33, 1, 0.20, 0.3
				Rectangle:
					size: self.size
					pos: self.pos
			color: 1, 1, 1, 1
			orientation: 'vertical'
			Button:
				text: "MARIE GOLD"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
				on_release: root.mariegold()
			Button:
				text: "ROSE"
				background_normal: ''
				background_color: 0.33, 1, 0.20, 0.3
				on_release: root.rose()
		BoxLayout:
			orientation: 'vertical'
			size_hint_y: None
			height: "400dp"
			Label:
				id: disp_label
				text: ''
				canvas:
					Color:
						rgba: 0.33, 1, 0.20, 0.3
					Rectangle:
						size: self.size
						pos: self.pos
				color: 1, 1, 1, 1


<ConfirmPopup>:
    cols:1
	Label:
		text: root.text
		color: 0.33, 1, 0.20, 0.3
		font_size: '20sp'
	GridLayout:
		cols: 2
		size_hint_y: None
		height: '44sp'
		spacing: [2,2]
		Button:
			text: 'Yes'
			on_release: root.dispatch('on_answer','yes')
			background_normal: ''
			background_color: 0.2, 0.2, 0.2, 1
		Button:
			text: 'No'
			on_release: root.dispatch('on_answer', 'no')
			background_normal: ''
			background_color: 0.2, 0.2, 0.2, 1

''')


class Iotsgh(App):

	def build(self):
		return root_widget

	def on_pause(self):
		return True
	def on_resume(self):
		pass


Iotsgh().run()
