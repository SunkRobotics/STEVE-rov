import os
from smbus2 import SMBus


def focus(distance):
    value = (distance << 4) & 0x3ff0
    byte1 = (value >> 8) & 0x3f
    byte2 = value & 0xf0
    data = [byte1, byte2]
    print(data)
    with SMBus(1) as bus:
        bus.write_i2c_block_data(12, 0, data)


def main():
    while True:
        focal_distance = int(input("Focal Distance: "))
        focus(focal_distance)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
