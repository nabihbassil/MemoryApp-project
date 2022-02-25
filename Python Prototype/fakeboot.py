# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network

ssid = "Nabih"
password = "test1234"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass

print('network config:', wlan.ifconfig())

# ************************
# Web Server in ESP32 using
# web sockets (wifi station)
# Author: George Bantique
# Date: October 28, 2020
# Feel free to modify it
# according to your needs
# ************************
import time
import machine
from hcsr04 import HCSR04
from time import sleep
from machine import Pin
import neopixel

# ************************
# Configure the ESP32 wifi
# as STAtion mode.
import network

first=0

#LED lights
np = neopixel.NeoPixel(Pin(21, Pin.OUT), 22)
count = 0

# Distance
sensor = HCSR04(trigger_pin=17, echo_pin=18, echo_timeout_us=1000000)

#motor
p4 = machine.Pin(17)
servo = machine.PWM(p4,freq=50)

sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    #sta.connect('your wifi ssid', 'your wifi password')
    sta.connect('Tenda_6F1750', 'geoven021110')
    while not sta.isconnected():
        pass
print('network config:', sta.ifconfig())

# ************************
# Configure the socket connection
# over TCP/IP
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable 
#                 by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

# ************************
# Function for creating the
# web page to be displayed
def ultra(ii):
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')
    if ii == 15 :
        servo.duty(110)
        sleep(2)
        servo.duty(60)
        print("ruuuuuuuuuuuuuuuuuuuuuunnn")
    
    if distance > 6.2 :
        first = 1
        count = 21
        for i in np:
            if count > 14:
                np[count] = (205, 70, 10) # set to green, half brightness
                count= count - 1

        np.write()
        ii = ii + 1
        return ii
        


    else:
        print("distance too far ",ii," is ii")
        count = 21
        if ii > 0:
            print("but its been opened before")
            for i in np:
                if count > 14:
                    np[count] = (83, 28, 4) # set to green, half brightness
                    count= count - 1
        else:
            print("not opened before")
            for i in np:
                if count > 14:
                    np[count] = (0, 0, 0) # set to green, half brightness
                    count= count - 1
        
        np.write()
        ii = ii + 1
        return ii


def web_page():
    html_page = """    
    <html>    
    <head>    
     <meta content="width=device-width, initial-scale=1" name="viewport"></meta>    
    </head>    
    <body style='background-color:#1ABC9C;display: flex; justify-content: center; align-items: center;  text-align: center; min-height: 100vh;  flex-direction: column;'>    
     <center><h1 style='font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; color:white; font-size: 4em !important;'>Thank you for your memory! </h1>
     <h4 style='font-family: "Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; color:white; font-size: 2em;'> This tab will be closed shortly. <br> The memory box will open to save your souvenir once you are back home.</h4></center>      
    </body>
     <script type="text/javascript">
      setTimeout(function() {
      window.close()
      }, 5000);
    </script>
    </html>"""
    print(html_page)
    return html_page   

tim0 = machine.Timer(0)
def handle_callback(timer):
    led.value( not led.value() )
isLedBlinking = False

while True:
    
    # Socket accept() 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("Content %s" % str(request))
    # Socket send()
    
         
    response = web_page()
    print("who let the dogs out")
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    sleep(10)
    print("Heeellllllllloooooooooooooooooooooooooooooooooooooooooooooooooooo")
    servo.duty(110)
    sleep(2)
    servo.duty(60)
    sleep(2)
    while True:
        first = ultra(first)  
        sleep(3)
    # Socket close()
