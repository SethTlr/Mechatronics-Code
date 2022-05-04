import numpy as np

from MotorControl import MotorContol
from Controler import handle_joystick
import pygame

#
# max_speed = 2048
# ratio_of_turn = 0.25  # 0 to 1
#
# max_offset = max_speed * ratio_of_turn
# max_motor_speed = max_speed - max_offset
#
# joy_max = 0
# joy_min = 0



class linear_map:
    def __init__(self, in_max, in_min, out_max, out_min):
        self.imin = in_min
        self.imax = in_max
        self.omin = out_min
        self.omax = out_max
        self.del_in = in_max - in_min
        self.del_out = out_max - out_min
        # normalize
        self.in_dir = self.del_in / np.absolute(self.del_in)
        # self.out_dir = self.del_out / np.absolute(self.del_out)

    def map(self, val):
        if self.in_dir > 0:
            if val < self.imin:
                return self.omin
            if val > self.imax:
                return self.omax
        else:
            if val > self.imin:
                return self.omin
            if val < self.imax:
                return self.omax

        precent = (val-self.imin) / self.del_in
        return self.del_out * precent + self.omin


def tele(joy, motor, max_motor_speed, max_offset):
    max_speed = max_motor_speed + max_offset
    # Max, Min, Max_out, Min_out
    xmap = linear_map(-1.0, 0, max_speed, 0)

    ymap = linear_map(1.0, -1.0, max_offset, -max_offset)

    while True:
        # get joystick's
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            (Axis_values, Button_values, Hats_values) = joy.update()

            # kill
            if Button_values[6] or Button_values[4]:  # left side of joystick
                return "exit"

            if Button_values[5] or Button_values[7]:
                return "auto"

            x, y = Axis_values[1], Axis_values[0]
            x, y = xmap.map(x), ymap.map(y)
            print(f"X Map: {x} | Y Map: {y}")

            # motor.run(x, y)
