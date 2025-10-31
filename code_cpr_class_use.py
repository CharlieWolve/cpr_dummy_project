import time
import board # type: ignore
import busio # type: ignore
import adafruit_vcnl4200 # type: ignore
import project_rgb_led as rgb
import project_calibrate_depth as calib
import project_calculate_frequency as calc
import project_frequency_training as f_training

# Rekalibrierungsfunktion
# 2. LED für Rythmus
# bpm Messung

depth_rgb_gp = [board.GP2, board.GP1, board.GP0]
bpm_rgb_gp = [board.GP10, board.GP11, board.GP12]
button_gp = board.GP8
i2c = busio.I2C(scl=board.GP27, sda=board.GP26)
sensor = adafruit_vcnl4200.Adafruit_VCNL4200(i2c)

depth_led = rgb.RGB_LED(depth_rgb_gp)
bpm_led = rgb.RGB_LED(bpm_rgb_gp)
depth_calibration = calib.Calibrate(depth_led, bpm_led, button_gp, sensor)
frequency_calculation = calc.Calculate(depth_led, bpm_led, depth_calibration.threshold_dict, sensor)
training = f_training.Training(depth_led, bpm_led, depth_calibration.threshold_dict, sensor)


# Signal that programm is ready
def on_signal():
    for i in range(4):
        depth_led.set_green()
        bpm_led.set_green()
        time.sleep(0.1)
        depth_led.set_off()
        bpm_led.set_off()
        time.sleep(0.1)

def start_signal():
    for i in range(2):
        depth_led.set_white()
        bpm_led.set_white()
        time.sleep(0.1)
        depth_led.set_off()
        bpm_led.set_off()
        time.sleep(0.1)

def training_signal():
    for i in range(2):
        depth_led.set_cyan()
        bpm_led.set_cyan()
        time.sleep(0.1)
        depth_led.set_off()
        bpm_led.set_off()
        time.sleep(0.1)

on_signal()
print("Ready!")
training_mode = False
true_start = False

while True:    
    if not depth_calibration.button_raised.value:
        if not depth_calibration.calibrated:
            depth_calibration.calibrate()
        else: 
            time.sleep(1.5)
            if not depth_calibration.button_raised.value:
                training_mode = True
                training_signal()
            else: 
                true_start = not true_start
                if true_start:
                    start_signal()
                else:
                    on_signal()
                training_mode = False
        time.sleep(0.1)
    elif true_start and frequency_calculation.press_end:
        if sensor.proximity > frequency_calculation.top + 5:
            frequency_calculation.update()
        time.sleep(0.05)
    elif training_mode and training.press_end:
        if sensor.proximity > frequency_calculation.top + 5:
            training.update()
        time.sleep(0.05)
        training.time_check()
    else:
        time.sleep(0.05)
        