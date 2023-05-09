import asyncio
import json
import time
from motors import Motors
#  from ms5837 import MS5837_30BA
import websockets


# websocket server
class WSServer:
    # registers the websocket objects of the clients to allow sending data to
    # the clients outside of the handler function
    joystick_client = None
    # web client websocket object used to transmit non-image data (sensor data)
    web_client_main = None
    # separate websocket used to transmit binary image data
    web_client_camera = None

    # incoming joystick data, can be accessed outside of the handler function
    joystick_data = None

    @classmethod
    def pump_joystick_data(cls):
        return cls.joystick_data

    @classmethod
    async def joystick_handler(cls, websocket, path):
        cls.joystick_client = websocket
        print("Joystick client connected")
        async for message in websocket:
            cls.joystick_data = json.loads(message)
        cls.joystick_client = None

    @classmethod
    async def web_client_main_handler(cls, websocket, path):
        cls.web_client_main = websocket
        print("Web client connected!")
        while True:
            try:
                await websocket.wait_closed()
                print("Web client disconnected!")
                cls.web_client_main = None
                break
            except websockets.ConnectionClosed:
                print("Web client disconnected!")

    @classmethod
    async def web_client_camera_handler(cls, websocket, path):
        cls.web_client_camera = websocket
        print("Web client connected!")
        while True:
            try:
                await websocket.wait_closed()
                print("Web client disconnected!")
                cls.web_client_camera = None
                break
            except websockets.ConnectionClosed:
                print("Web client disconnected!")

    @classmethod
    async def handler(cls, websocket, path):
        try:
            client_info_json = await asyncio.wait_for(websocket.recv(),
                                                      timeout=2.0)
            print("Client connected!")
        except asyncio.TimeoutError:
            print("Connection failed!")
            return
        client_info = json.loads(client_info_json)
        try:
            client_type = client_info["client_type"]
        except KeyError:
            print("Key error!")
            return
        if client_type == "joystick":
            await cls.joystick_handler(websocket, path)
        elif client_type == "web_client_main":
            await cls.web_client_main_handler(websocket, path)
        elif client_type == "web_client_camera":
            await cls.web_client_camera_handler(websocket, path)


# used to adjust the motor velocities to keep the ROV at a constant position
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

    # takes in the acceleration as the process value
    def compute(self, process_value):
        current_time = time.time()
        d_time = time.time() - self.last_time
        self.last_time = current_time

        # difference between the target and measured acceleration
        error = self.set_point - process_value
        # compute the integral ∫e(t) dt
        self.error_sum += error * d_time
        # compute the derivative
        d_error = (error - self.last_error) / d_time
        self.last_error = error

        # add the P, I, and the D together
        output = (self.proportional_gain * error + self.integral_gain
                  * self.error_sum + self.derivative_gain * d_error)
        return output


async def main_server():
    motors = Motors()
    #  depth_sensor =
    # adjust the y-velocity to have the ROV remain at a constant depth
    #  vertical_anchor = False
    #  vertical_pid = PID(0, 0.4, 3, 0.001)
    # stores the last button press of the velocity toggle button
    prev_speed_toggle = None
    # multiplier for velocity to set speed limit
    speed_factor = 0.5

    #  prev_anchor_toggle = None

    print("Server started!")
    while True:
        joystick_data = WSServer.pump_joystick_data()

        # if a joystick client hasn't connected yet
        if not joystick_data:
            await asyncio.sleep(0.01)
            continue

        x_velocity = joystick_data["left_stick"][0] * speed_factor
        # the joystick interprets up as -1 and down as 1, the negative just
        # reverses this so up is 1 and down is -1
        y_velocity = joystick_data["left_stick"][1] * speed_factor
        z_velocity = -joystick_data["right_stick"][1] * speed_factor
        yaw_velocity = joystick_data["right_stick"][0] * speed_factor
        roll_velocity = joystick_data["dpad"][0] * speed_factor
        #  gripper_grab = (joystick_data["buttons"]["right_trigger"]
        #                  - joystick_data["buttons"]["left_trigger"])
        # rotate left if negative, rotate right if positive
        #  gripper_rotate = (joystick_data["buttons"]["right_bumper"]
        #                    - joystick_data["buttons"]["left_bumper"])
        speed_toggle = joystick_data["dpad"][1]
        #  anchor_toggle = joystick_data['buttons'][11]

        # if vertical_anchor:
        # arduino_commands["y"] = vertical_pid.compute(
        # arduino_data["z_accel"])

        motors.drive_motors(x_velocity, y_velocity, z_velocity, yaw_velocity,
                            roll_velocity)

        # increase or decrease speed when the dpad buttons are pressed
        if speed_toggle != prev_speed_toggle:
            # make sure the speed doesn't exceed 1
            if speed_toggle > 0 and speed_factor < 1:
                speed_factor *= 2
            # make sure the speed doesn't fall below 0.125
            if speed_toggle < 0 and speed_factor >= 0.125:
                speed_factor /= 2

            # just in case the speed factor ends up out of range
            if speed_factor > 1:
                speed_factor = 1
            elif speed_factor < 0:
                speed_factor = 0
            prev_speed_toggle = speed_toggle

        # toggle the vertical anchor
        #  if anchor_toggle == 1 and prev_anchor_toggle == 0:
        #      if vertical_anchor:
        #          vertical_anchor = False
        #      else:
        #          vertical_anchor = True
        #  prev_anchor_toggle = anchor_toggle

        await asyncio.sleep(0.01)


def main():
    loop = asyncio.get_event_loop()
    ws_server = websockets.serve(
        WSServer.handler, "0.0.0.0", 8765, ping_interval=None)
    asyncio.ensure_future(ws_server)
    asyncio.ensure_future(main_server())
    loop.run_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('')
