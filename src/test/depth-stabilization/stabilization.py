#!/usr/bin/python
import motors.py
import ms5837
import time

class PID:
    last_time = None
    last_error = None
    error_sum = 0

    def __init__(self, set_point, proportional_gain, integral_gain,
                 derivative_gain):
        self.set_point = set_point
        self.proportional_gain = proportional_gain
        self.integral_gain = integral_gain
        self.derivative_gain = derivative_gain

        self.last_time = time.time()
        self.last_error = set_point

    def compute(self, process_value):
        current_time = time.time()
        d_time = time.time() - self.last_time
        print(f"Change in Time: {d_time}")
        self.last_time = current_time

        error = self.set_point - process_value
        print(f"Error: {error}")

        # compute the integral
        self.error_sum += error * d_time
        print(f"Error: {self.error_sum}")

        # compute the derivative
        d_error = (error - self.last_error) / d_time
        print(f"d_error: {d_error}")
        print(f"Adjusted d_error: {d_error * self.derivative_gain}")
        self.last_error = error

        output = (self.proportional_gain * error + self.integral_gain
                  * self.error_sum + self.derivative_gain * d_error)
        print(f"Output: {output}")
        return output


class Plant:
    plant_state = 0

    def __init__(self, initial_state):
        self.plant_state = initial_state

    def process(self, actuating_signal):
        self.plant_state -= 10
        self.plant_state += actuating_signal
        return self.plant_state
depth_sensor = ms5837.MS5837_02BA(1)

# initialize the sensor before reading it
if not depth_sensor.init():
    print("Depth sensor could not be initialized")
    exit(1)



