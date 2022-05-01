from Controler import handle_joystick
from MotorControl import MotorContol
from Tele import tele
from Auto import auto

max_speed = 2048
ratio_of_turn = 0.25  # 0 to 1

max_offset = max_speed * ratio_of_turn
max_motor_speed = max_speed - max_offset




def main():
    Left_Motor_Pin = 12
    Right_Motor_Pin = 13

    joy = handle_joystick()
    motors = MotorContol(max_motor_speed, max_offset, Left_Motor_Pin, Right_Motor_Pin)

    (Axis_values, Button_values, Hats_values) = joy.update()

    while True:
        #send to tell
        if tele(joy, motors, max_motor_speed, max_offset) == "exit":
            break
        #send to auto
        auto(joy, motors, max_motor_speed, max_offset)


if __name__ == "__main__":
    main()