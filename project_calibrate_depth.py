import time
import math
import digitalio # type: ignore
from project_rgb_led import RGB_LED
from project_statistics import mean, stdev
from adafruit_vcnl4200 import Adafruit_VCNL4200 # type: ignore 
from board import Pin # type: ignore 
# correct import? 


class Calibrate:
    
    def __init__(self, depth_led: RGB_LED, bpm_led: RGB_LED, button_gp: Pin, sensor: Adafruit_VCNL4200) -> None:
        self.button_raised = digitalio.DigitalInOut(button_gp)
        self.button_raised.switch_to_input(pull=digitalio.Pull.UP)
        self.sensor = sensor
        self.depth_led = depth_led
        self.bpm_led = bpm_led
        self.calibrated = False
        self.threshold_dict = {"fourty": 0, "fourtyfive": 0, "fiftyfive": 0, "sixty": 0}

    def color_selection(self, led: RGB_LED) -> None:
        if self.threshold_dict["fourty"] == 0:
            led.set_red()
        elif self.threshold_dict["fourtyfive"] == 0:
            led.set_yellow()
        elif self.threshold_dict["fiftyfive"] == 0:
            led.set_green()
        elif self.threshold_dict["sixty"] == 0:
            led.set_blue()

    def calibration_signal(self) -> None:
        self.color_selection(self.depth_led)
        self.color_selection(self.bpm_led)
        time.sleep(0.15)
        self.depth_led.set_off()
        self.bpm_led.set_off()
        time.sleep(0.15)

    def check_for_stop(self) -> float:
        self.calibration_signal()
        first_proximity = self.sensor.proximity
        last_proximities = [first_proximity]
        last_proximities.append(first_proximity)
        self.calibration_signal
        last_proximities.append(self.sensor.proximity)
        self.calibration_signal
        deviation = stdev(last_proximities)
        old_time = time.monotonic()
        new_time = time.monotonic()
        time_diff = new_time - old_time
        while time_diff < 3:
            if deviation > 5 and self.sensor.proximity > first_proximity +5: 
                old_time = new_time
                new_time = time.monotonic()
                time_diff = new_time - old_time    
            else:
                new_time = time.monotonic()
                time_diff = new_time - old_time
            self.calibration_signal()
            last_proximities.pop(0)
            last_proximities.append(self.sensor.proximity)
            deviation = stdev(last_proximities)      
        return mean(last_proximities)
    
    def get_calibration_distance(self)-> int:
        self.depth_led.set_off()
        self.bpm_led.set_off()
        target_mean = self.check_for_stop()
        return math.floor(target_mean)
        
    def calibrate(self) -> None:
        self.recalibration_check()
        distance = self.get_calibration_distance()
        if self.threshold_dict["fourty"] == 0:
            self.threshold_dict["fourty"] = distance
        elif self.threshold_dict["fourtyfive"] == 0:
            self.threshold_dict["fourtyfive"] = distance
        elif self.threshold_dict["fiftyfive"] == 0:   
            self.threshold_dict["fiftyfive"] = distance
        elif self.threshold_dict["sixty"] == 0:
            self.threshold_dict["sixty"] = distance
            self.calibrated = True
        print(self.threshold_dict)
    
