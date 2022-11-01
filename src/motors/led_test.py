import adafruit_motor.servo
import adafruit_pca9685
import board
import busio
import time

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 255
led_channel = pca.channels[8]

led_channel.duty_cycle = 1000
#  for i in range(32767):
#      led_channel.duty_cycle = i
#      time.sleep(0.001)

#  for i in range(32767, 0, -1):
#      led_channel.duty_cycle = i
#      time.sleep(0.001)
