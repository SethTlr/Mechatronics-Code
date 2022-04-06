import threading
import time

class PID:
    previous_time =0.0
    previous_error=0.0
    sum_error=0.0
    Integral=0.0
    D_cycle=10

    def __init__(self, P, I, D, cycle ):
        self.P = P
        self.I = I
        self.D = D
        self.error = 0

    # def update(self, Error, time):
    #     last_error = self.error
    #     self.error = Error
    #
    #     # P - Preportinal
    #     Pout = (self.P / 10 * error)
    #
    #     # I -
    #     Iout = (self.I
    #
    #
    #     # D -
    #     Dout = (Error - last_error)*self.D




    def correct(self, kp, ki, kd, error):
        if (self.previous_time == 0):
            self.previous_time = time.time()
        current_time = time.time()

        #P- Preportinal
        Pout = (kp / 10 * error)

        #I- Intagral
        delta_time = current_time - self.previous_time
        self.Integral += (error * delta_time)
        if self.Integral > 10:
            self.Integral = 10
        if self.Integral < -10:
            self.Integral = -10
        Iout=(ki/10) * self.Integral)

        #D- Derivitive
        delta_error = error - self.previous_error
        Derivative = (delta_error / delta_time)

        Dout = ((kd / 1000) * Derivative)

        output += Pout + Dout + Iout

        self.previous_time = current_time
        self.previous_error = error
        self.sum_error += error

        if ((output > self.D_cycle) & (self.D_cycle < 90)):
            self.D_cycle += 1

        if ((output < self.D_cycle) & (self.D_cycle > 10)):
            self.D_cycle -= 1

        return output
