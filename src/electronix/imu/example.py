# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bno055


def main():
    i2c = board.I2C()
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    prev_accel_y = []
    prev_accel_z = []
    prev_accel_x = []

    x_velocity = 0
    count = 0
    while True:
        accel_x, accel_y, accel_z = sensor.acceleration
        if accel_x is None or accel_y is None or accel_z is None:
            continue

        avg_accel_x = 0
        prev_accel_x.append(accel_x - 0.021)
        avg_accel_x = sum(prev_accel_x) / len(prev_accel_x)
        #  if len(prev_accel_x) > 1000:
        #      prev_accel_x.pop(0)

        prev_accel_y.append(accel_y)
        if len(prev_accel_y) > 5:
            prev_accel_y.pop(0)

        prev_accel_z.append(accel_z)
        if len(prev_accel_z) > 5:
            prev_accel_z.pop(0)

        #  avg_accel_y = sum(prev_accel_y) / len(prev_accel_y)
        #  avg_accel_z = sum(prev_accel_z) / len(prev_accel_z)

        x_velocity += avg_accel_x

        print(avg_accel_x)
        #  print(x_velocity)
        #  print(f'{avg_accel_z:.2f}')
        count += 1
        time.sleep(0.01)


if __name__ == "__main__":
    main()
