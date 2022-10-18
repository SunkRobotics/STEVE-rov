# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bno055

def main():
    i2c = board.I2C()
    sensor = adafruit_bno055.BNO055_I2C(i2c)

    # If you are going to use UART uncomment these lines
    # uart = board.UART()
    # sensor = adafruit_bno055.BNO055_UART(uart)

    last_val = 0xFFFF


    def temperature():
        global last_val  # pylint: disable=global-statement
        result = sensor.temperature
        if abs(result - last_val) == 128:
            result = sensor.temperature
            if abs(result - last_val) == 128:
                return 0b00111111 & result
        last_val = result
        return result

    
    while True:
        print(sensor.acceleration)
        time.sleep(0.05)

if __name__ == "__main__":
    main()
