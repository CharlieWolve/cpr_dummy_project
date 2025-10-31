import time
import math
from project_rgb_led import RGB_LED
from adafruit_vcnl4200 import Adafruit_VCNL4200 # type: ignore 

class Calculate:
    
    def __init__(self, depth_led: RGB_LED, bpm_led: RGB_LED, depth_dict: dict, sensor: Adafruit_VCNL4200) -> None:
        self.f_list = []
        self.d_dict = depth_dict
        self.sensor = sensor
        self.depth_led = depth_led
        self.bpm_led = bpm_led
        self.mean_freq = 0
        self.press_end = True
        self.prev_press_time = 0
        self.delta_press_time = 0        
        self.top = self.sensor.proximity
    
    def color_choice_freq(self, freq) -> None:
        if freq <= 100:
            self.bpm_led.set_red()
        elif 100 < freq <= 105:
            self.bpm_led.set_yellow()
        elif 105 < freq <= 115:
            self.bpm_led.set_green()
        elif 115 < freq <= 120:
            self.bpm_led.set_purple()
        elif 120 <= freq:
            self.bpm_led.set_blue()
        else:
            self.bpm_led.set_off()
    
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
            
    def frequency_mean(self, freq):
        print(self.f_list)
        self.f_list = [freq] + self.f_list
        if len(self.f_list) > 3:
            self.f_list.pop()
        return math.floor(sum(self.f_list) / len(self.f_list))
    
    def refresh_time_values(self) -> None:
        print(f'previous: {self.prev_press_time}')
        time_now = time.monotonic()
        print(f'time: {time_now}')
        self.delta_press_time = time_now - self.prev_press_time
        print(f'delta: {self.delta_press_time}')
        self.prev_press_time = time_now
        
    def calculation(self) ->None:
        if self.prev_press_time != self.delta_press_time:
            frequency = math.floor(1 / (self.delta_press_time / 60))
            self.mean_freq = self.frequency_mean(frequency)
            print(f"frequencies: {self.f_list}, mean: {self.mean_freq}")
            self.color_choice_freq(self.mean_freq)

    def update(self) -> None:
        self.press_end = False
        self.refresh_time_values()
        prev_prox = self.sensor.proximity
        while self.sensor.proximity > prev_prox - 5:
            print(f'old_prox: {prev_prox}')
            prev_prox = self.sensor.proximity
            print(f'new_prox: {prev_prox}')
            time.sleep(0.01)
        print(f"proximity: {prev_prox}")
        self.color_choice_depth(prev_prox)
        self.calculation()
        while not self.press_end:
            if self.sensor.proximity < self.top + 5:  # standard (completely decompressed)#
                self.press_end = True
            time.sleep(0.02)
        