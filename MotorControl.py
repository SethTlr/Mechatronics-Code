import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class MotorContol:
    max, min = 100, 0

    def __init__(self, max_speed, max_offset, l_pin, r_pin):
        freq = 1000
        # setting up pins
        GPIO.setup(l_pin, GPIO.OUT)
        GPIO.setup(r_pin, GPIO.OUT)
        self.l_pwm = GPIO.PWM(l_pin, freq)
        self.r_pwm = GPIO.PWM(r_pin, freq)
        self.l_pwm.start(0)
        self.r_pwm.start(0)

        # setting range
        self.scale = 1 / (max_speed + max_offset)

    def bound(self, value):
        if value > self.max:
            return self.max
        elif value < self.min:
            return self.min
        else:
            return value

    def run(self, speed, offset):  # speed: 0-100 turn: -100-100
        l_duty = (speed + offset) * self.scale
        r_duty = (speed - offset) * self.scale
        l_duty = self.bound(l_duty)
        r_duty = self.bound(r_duty)
        self.l_pwm.ChangeDutyCycle(l_duty)
        self.r_pwm.ChangeDutyCycle(r_duty)