import time
import board
import busio
import adafruit_vcnl4200
import project_rgb_led as rgb
import project_calibrate_depth as calib
import project_calculate_frequency as calc

# Rekalibrierungsfunktion
# 2. LED für Rythmus
# bpm Messung

depth_rgb_gp = [board.GP2, board.GP1, board.GP0]
bpm_rgb_gp = [board.GP10, board.GP11, board.GP12]
button_gp = board.GP8
i2c = busio.I2C(scl=board.GP27, sda=board.GP26)
sensor = adafruit_vcnl4200.Adafruit_VCNL4200(i2c)
# 
depth_led = rgb.RGB_LED(depth_rgb_gp)
bpm_led = rgb.RGB_LED(bpm_rgb_gp)
depth_calibration = calib.Calibrate(depth_led, bpm_led, button_gp, sensor)
frequency_calculation = calc.Calculate(depth_led, bpm_led, depth_calibration.threshold_dict, sensor)


# Signal that programm is ready
def on_signal():
    for i in range(4):
        depth_led.set_green()
        bpm_led.set_green()
        time.sleep(0.1)
        depth_led.set_off()
        bpm_led.set_off()
        time.sleep(0.1)


on_signal()

while True:    
    if not depth_calibration.button_off.value:
        depth_calibration.calibrate()
        five_cm_mark = depth_calibration.five_cal
        six_cm_mark = depth_calibration.six_cal
        time.sleep(0.1)
    elif depth_calibration.calibrated and frequency_calculation.press_end:
        if sensor.proximity > frequency_calculation.top + 5:
            frequency_calculation.press_end = False
            frequency_calculation.update()
        time.sleep(0.02)
    else:
        time.sleep(0.1)