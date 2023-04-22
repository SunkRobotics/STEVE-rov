from machine import Pin
#import time                                                                                                           `
import network
import socket
import re

def drive_motors(wait_length):
    dir_pin = Pin(17, Pin.OUT)
    pwm_pin = Pin(16, Pin.OUT)
    
    dir_pin.on() # extending
    pwm_pin.on() # turning motor on to full speed
    time.sleep(5) # waiting for float to be fully extended
    pwm_pin.off() # turning of motor
    time.sleep(wait_length) # gliding for the specified time
    dir_pin.off() # retracting 
    pwm_pin.on() # turning motor on
    time.sleep(5) # waiting for motor to retract
    pwm_pin.off() # stopping motor and waiting for further instuction
    

def uri_parser(uri):
    # parsing the uri based on the input boxes in
    # www/index.html
    # if the uri is "break" then it will break the webserver loop
    try:
        wait_length = uri.split("=")[1]
        print(wait_length)
        drive_motors(float(wait_length))
    except:
        print("no uri")
    
def webserver():
    #  a very simple custom webserver because the existing
    # alternatives are too complex for my purposes
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    print("binded")
    s.listen(1)

    print('listening on', addr)

    file = open("index.html", "r")  # getting html page from index.html
    html = file.read()  # converting the file pointer into a string

    # Starting a infinate webserver loop
    while True:
        # accepting connection
        conn, addr = s.accept()
        print('client connect from', addr)

        # receiving 1024 bytes of data
        request = conn.recv(1024)

        # filtering get requesting using magic regex
        match = re.search("GET\s+(\S+)\s+", request.decode())
        uri = match.group(1)
        uri = uri.replace("/", "")  # getting rid of the "/" in the uri

        # sending http request
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(html)  # sending the html
        conn.close()  # closing the connection
        uri_parser(uri)  # parsing the uri
    # close the socket
    s.close()


wlan = network.WLAN(network.AP_IF)
wlan.config(essid="test", key="password")
wlan.active(True)
# print information for connecting to network
print("SSID:", wlan.config("essid"))
print(wlan.ifconfig())

webserver()
