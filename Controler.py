import pygame, sys
from time import sleep


class handle_joystick:
	def __init__(self):
		self.joystick_count = pygame.joystick.get_count()
		
		if self.joystick_count == 0:
			# if no joysticks, quit program safely
			print ("Error, I did not find any joysticks")
			pygame.quit()
			sys.exit()
		else:
			# initialise joystick
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()
		
		
		self.axes = self.joystick.get_numaxes()
		self.buttons = self.joystick.get_numbuttons()
		self.hats = self.joystick.get_numhats()
	
	def getAxis(self, number):
		# when nothing is moved on an axis, the VALUE IS NOT EXACTLY ZERO
		# so this is used not "if joystick value not zero"
		val = self.joystick.get_axis(number)
		if (val < -0.1) or (val > 0.1):
			# value between 1.0 and -1.0
			print(f"Axis value is {val} | Axis ID is {number}")
		return val


	def getButton(self, number):
		# returns 1 or 0 – pressed or not
		value = self.joystick.get_button(number)
		if value:
			# just prints id of button
			print(f"Button ID is {number}")
		return value


	def getHat(self, number):
		value = self.joystick.get_hat(number)
		if value != (0,0):
			# returns tuple with values either 1, 0 or -1
			print(f"Hat value is {value[0]}, {value[1]} | Hat ID is {number}")
		return value
	
	def update(self):
		Axis_values = []
		Button_values = []
		Hats_values = []
		
		if self.axes != 0:
			for i in range(self.axes):
				Axis_values.append(self.getAxis(i))
		if self.buttons != 0:
			for i in range(self.buttons):
				Button_values.append(self.getButton(i))
		if self.hats != 0:
			for i in range(self.hats):
				Hats_values.append(self.getHat(i))
		
		return [Axis_values, Button_values, Hats_values]


pygame.init()
joy = handle_joystick()
joy_values = []

      
while True:
	for event in pygame.event.get():
		# loop through events, if window shut down, quit program
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		joy_values = joy.update()
		print(joy_values)
      
