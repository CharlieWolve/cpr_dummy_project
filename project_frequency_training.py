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


    def time_check(self) -> None:
        if self.current_time - self.prev_time >= self.training_period:
            self.prev_time = time.monotonic()
        if self.current_time - self.led_on_time >= 0.1:
            self.bpm_led.set_off()
        else:
            self.bpm_led.set_cyan()
            self.current_time = time.monotonic()
            self.led_on_time = self.current_time


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
            time.sleep(0.02)
            self.time_check()
        