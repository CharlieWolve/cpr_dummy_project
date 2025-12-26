import time
from project_rgb_led import RGB_LED
from adafruit_vcnl4200 import Adafruit_VCNL4200 # type: ignore 

class Training:
    
    def __init__(self, depth_led: RGB_LED, bpm_led: RGB_LED, depth_dict: dict, sensor: Adafruit_VCNL4200) -> None:
        self.d_dict = depth_dict
        self.sensor = sensor
        self.depth_led = depth_led
        self.bpm_led = bpm_led
        self.training_period = 0.5  # 0.5 s time period translates to 120 bpm
        self.press_end = True      
        self.top = self.sensor.proximity
        self.prev_time = 0
        self.current_time = 0
        self.led_on_time = 0

    def color_choice_depth(self, proximity) -> None:
        if proximity <= self.d_dict["fourty"]:
            self.depth_led.set_red()
    #             print("red")
        elif self.d_dict["fourty"] < proximity <= self.d_dict["fourtyfive"]:
            self.depth_led.set_yellow()
    #             print("yellow")
        elif self.d_dict["fourtyfive"] < proximity <= self.d_dict["fiftyfive"]:
            self.depth_led.set_green()
    #             print("green")
        elif self.d_dict["fiftyfive"] < proximity <= self.d_dict["sixty"]:
            self.depth_led.set_purple()
    #             print("purple")
        elif self.d_dict["sixty"] <= proximity:
            self.depth_led.set_blue()
    #             print("blue")
        else:
            self.depth_led.set_off()

    def time_check(self) -> None:
        self.current_time = time.monotonic()
        if self.current_time - self.prev_time >= self.training_period:
            self.prev_time = time.monotonic()
            self.bpm_led.set_cyan()    
            self.led_on_time = self.current_time
        elif self.current_time - self.led_on_time >= 0.05:
            self.bpm_led.set_off()


    def update(self) -> None:
        self.press_end = False
        prev_prox = self.sensor.proximity
        while self.sensor.proximity > prev_prox - 5:
            prev_prox = self.sensor.proximity
            time.sleep(0.01)
            self.time_check()
        self.color_choice_depth(prev_prox)
        while not self.press_end:
            if self.sensor.proximity < self.top + 5:  # standard (completely decompressed)
                self.press_end = True
            time.sleep(0.01)
            self.time_check()
        