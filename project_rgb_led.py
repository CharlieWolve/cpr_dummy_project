import time
import digitalio # type: ignore

class RGB_LED:
    
    def __init__(self, GP_list: list) -> None:
        self.red_led = depth_red = digitalio.DigitalInOut(GP_list[0])
        self.red_led.direction = digitalio.Direction.OUTPUT
        self.green_led = depth_red = digitalio.DigitalInOut(GP_list[1])
        self.green_led.direction = digitalio.Direction.OUTPUT
        self.blue_led = depth_red = digitalio.DigitalInOut(GP_list[2])
        self.blue_led.direction = digitalio.Direction.OUTPUT                                  
        
    def set_yellow(self) -> None:
        self.red_led.value = True
        self.green_led.value = True
        self.blue_led.value = False
        
    def set_green(self) -> None:
        self.red_led.value = False
        self.green_led.value = True
        self.blue_led.value = False
        
    def set_red(self) -> None:
        self.red_led.value = True
        self.green_led.value = False
        self.blue_led.value = False
        
    def set_blue(self) -> None:
        self.red_led.value = False
        self.green_led.value = False
        self.blue_led.value = True
        
    def set_purple(self) -> None:
        self.red_led.value = True
        self.green_led.value = False
        self.blue_led.value = True
    
    def set_white(self) -> None:
        self.red_led.value = True
        self.green_led.value = True
        self.blue_led.value = True

    def set_cyan(self) -> None:
        self.red_led.value = False
        self.green_led.value = True
        self.blue_led.value = True
        
    def set_off(self) -> None:
        self.red_led.value = False
        self.green_led.value = False
        self.blue_led.value = False
    
    
    