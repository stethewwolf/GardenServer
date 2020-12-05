# File : command.py
# Author : stefano prina <stethewwolf@gmail.com>
# MIT License
# 
# Copyright (c) 2019 Stefano Prina
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from app_modules.core import LoggerFactory
from app_modules.core import SingleConfig
from app_modules.core import AppConstants
from app_modules.garden_server import Garden_Controller_Interface
import time

class Monitor():
    short_arg   = 'm'
    long_arg    = 'monitor'
    cmd_help    = 'Run application in monitor mode, in this mode the \
            application will compare the current soil moisture and if less then\
            treshold it will power on the pump [ DEFAULT ]'
    cmd_type    = None
    cmd_action  = 'store_true'

    def __init__(self, param=None):
        pass

    def run( self ):
        cfg = SingleConfig.getConfig()
        gci = Garden_Controller_Interface()

        soil_mositure = gci.get_soil_moiusture()
        light = gci.get_light()
        air_temperature = gci.get_temperature()
        air_moisture = gci.get_air_moisture()

        soil_moisture_guard = int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_MOISTURE_GUARD])

        print("=======================")
        print('Air temperature : {} C'.format(air_temperature))
        print('Air moisture : {} %'.format(air_moisture))
        print('Light idx ( 0 dark - 100 full light) : {}'.format(light))
        print('Soil moisture sensor 1 : {}'.format(soil_mositure))
        print('Soil moisture thresold : {}'.format(soil_moisture_guard))

        if soil_mositure <= soil_moisture_guard:

            print("start pump, watering for "+cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]+" sec")
            gci.set_pump_on()
            time.sleep(int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]))
            gci.set_pump_off()
            print("stop pump")

        print("=======================")
