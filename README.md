# cpr_dummy_project
Student project at TH Nürnberg Georg-Simon-Ohm to create a DIY reanimation Dummy for public use

To use this code on your Rasperry Pi Pico start by following this guide:
https://learn.adafruit.com/welcome-to-circuitpython
to set up your microcontroller. The project was created using version 9, so we suggest doing the same. 

Then download the adafruit libraries from their site: 
https://circuitpython.org/libraries
Download the bundle for Version 9.x on your computer. 

Once you have extracted the files choose the relevant libraries which are: 
- adafruit_register (folder)
- adafruit_io (folder)
- adafruit_bus_device (folder)
- adafruit_vcnl4200 (mpy-file)

copy these libraries onto your microcontroler in a 'lib' folder

Once done copy the code from 'code_cpr_class_use.py' into the code.py file and add the rest of our files (project_xxx.py) into the library folder.

Once the microcontroller is connected to the soldered board everything should be good to go.
