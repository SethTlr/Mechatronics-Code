import threading
import time

class PID:
    previous_time =0.0
    previous_error=0.0
    #sum_error=0.0
    Integral=0.0
    max_integral=10
    #D_cycle=10

    def __init__(self, kp, ki, kd, max_offset):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_offset = max_offset


    def correct(self, error):
        if (self.previous_time == 0):
            self.previous_time = time.time()
        current_time = time.time()

        #P- Preportinal
        Pout = (self.kp / 10 * error)

        #I- Intagral
        delta_time = current_time - self.previous_time
        self.Integral += (error * delta_time)
        if self.Integral > self.max_integral:
            self.Integral = self.max_integral
        if self.Integral < -(self.max_integral):
            self.Integral = -(self.max_integral)
        Iout=(self.ki/10) * self.Integral

        #D- Derivitive
        delta_error = error - self.previous_error
        Derivative = (delta_error / delta_time)

        Dout = ((self.kd / 1000) * Derivative)

        output += Pout + Dout + Iout

        self.previous_time = current_time
        self.previous_error = error
        #self.sum_error += error

        #if ((output > self.D_cycle) & (self.D_cycle < 90)):
        #    self.D_cycle += 1

        #if ((output < self.D_cycle) & (self.D_cycle > 10)):
        #    self.D_cycle -= 1

        if output > max_output:
            output = max_output
            print("output exceeded max value")

        return output
