from MotorControl import MotorContol
from Controler import handle_joystick
#
# max_speed = 2048
# ratio_of_turn = 0.25  # 0 to 1
#
# max_offset = max_speed * ratio_of_turn
# max_motor_speed = max_speed - max_offset

joy_max = 0
joy_min = 0



class linear_map:
    def __init__(self, in_max, in_min, out_max, out_min):
        self.imax = in_max
        self.imin = in_min
        self.omax = out_max
        self.omin = out_min

    def map(self, val):
        per = (self.imax-val)/(self.imax-self.imin)
        return (self.omax-self.omin) * self.per + self.imin


def tele(joy, motor, max_motor_speed, max_offset):
    max_offset = max_motor_speed + max_offset
    xmap = linear_map(joy_max, joy_min, 0, max_speed)
    ymap = linear_map(joy_max, joy_min, -max_offset, max_offset)


    while True:
        # get joystick's
        (Axis_values, Button_values, Hats_values) = joy.update()

        #kill
        if Button_values[0]:
            return "break"

        if Button_values[1]:
            return "auto"

        x, y = Axis_values[0], Axis_values[1]
        x, y = xmap.map(x), ymap.map(y)
        motor.run(x, y)
