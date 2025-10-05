import time
import math
import project_rgb_led as rgb
import digitalio


class Calibrate:
    
    def __init__(self, depth_led: RGB_LED, bpm_led: RGB_LED, button_gp: Pin, sensor: Adafruit_VCNL4200) -> None:
        self.button_off = digitalio.DigitalInOut(button_gp)
        self.button_off.switch_to_input(pull=digitalio.Pull.UP)
        self.sensor = sensor
        self.depth_led = depth_led
        self.bpm_led = bpm_led
        self.five_cal = 0
        self.six_cal = 0
        self.calibrated = False
        self.threshold_dict = {}
    
    def calibration_signal(self) -> None:
        self.depth_led.set_purple()
        self.bpm_led.set_purple()
        time.sleep(0.15)
        self.depth_led.set_off()
        self.bpm_led.set_off()
        time.sleep(0.15)
    
    def get_calibration_distance(self)-> int:
        button_value = self.button_off.value
        self.depth_led.set_off()
        self.bpm_led.set_off()
        while button_value == self.button_off.value:
            self.calibration_signal()
        if self.button_off.value:
            target = self.sensor.proximity
            print(f'target: {target}')
            return target
        else:
            return 0
    
    def calculate_thresholds(self) -> None:
        diff = self.six_cal-self.five_cal
        if len(self.threshold_dict) > 2:
            self.threshold_dict = {}
        min_press = math.floor(self.five_cal - 0.5 * diff)
        self.threshold_dict["min"] = min_press
        max_press = math.ceil(self.five_cal + 0.5* diff)
        self.threshold_dict["max"] = max_press
        too_much_press = self.five_cal + diff
        self.threshold_dict["too_much"] = too_much_press
        not_enough_press = self.five_cal - diff
        self.threshold_dict["not_enough"] = not_enough_press
        for key, value in self.threshold_dict.items():
            print(f"{key}: {value}")
        
        
    def recalibration_check(self) -> None:
        if self.calibrated:
            self.five_cal = 0
            self.six_cal = 0
            self.calibrated = False
        
    def calibrate(self) -> None:
        self.recalibration_check()
        distance = self.get_calibration_distance()
        if self.five_cal == 0:
            self.five_cal = distance
            self.threshold_dict["five_cm"] = distance
        elif self.six_cal == 0:
            self.six_cal = distance
            self.threshold_dict["six_cm"] = distance
            self.calculate_thresholds()
            self.calibrated = True
    
        
