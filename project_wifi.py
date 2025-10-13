import os
import time
import ssl
import wifi
import socketpool
import microcontroller
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

ptr = 0
while not wifi.radio.connected:
    try:
        SSID, PASSWORD = os.getenv("WIFI_SSID"+str(ptr)), os.getenv("WIFI_PASSWORD"+str(ptr))
    except:
        SSID, PASSWORD = 'Null', 'Null'
    s = 5
    if ptr < os.getenv("WIFI_ROUTERS"): print(' ', end='')
    print(ptr, SSID, '.'*s, end=' ')
    try:
        print('WiFi Connecting.', end='')
        wifi.radio.connect(SSID, PASSWORD)
    except:
        ptr += 1
        print('\b\b\bon Failed.')
    if ptr > os.getenv("WIFI_ROUTERS"):
        try:
            wifi.radio.connect(SSID, PASSWORD)
        except TypeError:
            print("Could not find WiFi info. Check your settings.toml file!")
            raise

try:
    aio_username = os.getenv("ADAFRUIT_AIO_USERNAME")
    aio_key = os.getenv("ADAFRUIT_AIO_KEY")
except TypeError:
    print("Could not find Adafruit IO info. Check your settings.toml file!")
    raise

class Depth_Visualization:

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
        
    # linear function: y = mx + t
    def __init__(self) -> None:
        self.five_cm_mark = 0
        self.six_cm_mark = 0
        self.function_m = 0
        self.function_t = 0
        self.feednames = ["distance", "proximity"]
        
        pool = socketpool.SocketPool(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl.create_default_context())            
        # Initialize an Adafruit IO HTTP API object
        self.io = IO_HTTP(aio_username, aio_key, requests)
        print("\nConnected to io!")
        
    def create_linear_function(self) -> None:
        self.function_m = 1 / (self.six_cm_mark - self.five_cm_mark)
        self.function_t = 5 - self.function_m * self.five_cm_mark
    
    def create_feed(self, feed) -> None: 
        try:
        # get feed
            return self.io.get_feed(feed)
        except AdafruitIO_RequestError:
        # if no feed exists, create one
            return self.io.create_new_feed("distance")
    
    def start_connection(self, five_cm_mark, six_cm_mark) -> None:
        self.five_cm_mark = five_cm_mark
        self.six_cm_mark = six_cm_mark
        self.create_linear_function()
        for name in self.feednames:
            self.feedlist.append(self.create_feed(name))
            print(f'Feed {name} has been created')
    
    def microcontroller_reset() -> None: 
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()
    
    def send_proximity(self, proximity) -> None:
        distance = self.function_m * proximity + self.function_t
        self.io.send_data(self.feedlist[0]["key"], distance)
        self.io.send_data(self.feedlist[1]["key"], proximity)
