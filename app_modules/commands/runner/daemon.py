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

class Daemon():
    short_arg   = 'd'
    long_arg    = 'daemon'
    cmd_help    = 'Run application in daemon mode, in this mode the \
            application will compare the current soil moisture and if less then\
            treshold it will power on the pump periodically'
    cmd_type    = None
    cmd_action  = 'store_true'

    def __init__(self, param=None):
        self.cfg = SingleConfig.getConfig()
        self.gci = Garden_Controller_Interface()

    def run( self ):
        while True:
            soil_mositure_s1 = self.gci.get_soil_moiusture(1)
            soil_mositure_s2 = self.gci.get_soil_moiusture(2)
            light = self.gci.get_light()
            air_temperature = self.gci.get_temperature()
            air_moisture = self.gci.get_air_moisture()
            
            soil_moisture_guard = int(self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_MOISTURE_GUARD])

            if (soil_mositure_s1 <= soil_moisture_guard) or \
               (soil_mositure_s2 < soil_moisture_guard):
                print("start pump, watering for "+self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]+" sec")
                self.gci.set_pump_on()
                time.sleep(int(self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]))
                self.gci.set_pump_off()
                print("stop pump")

            time.sleep(int(self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_SLEEP_MIN])*60)
