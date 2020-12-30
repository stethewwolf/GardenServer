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

from app_modules.core import LoggerFactory, SingleConfig, AppConstants, AppDBIface
import app_modules.core.mqtt as Mqtt
from app_modules.garden_server import Fake_Controller_Interface
import time, json

class Daemon_Test():
    short_arg   = ''
    long_arg    = 'daemon-test'
    cmd_help    = 'Run application in daemon test mode, not require controller connected'
    cmd_type    = None
    cmd_action  = 'store_true'

    def __init__(self, param=None):
        self.logger = LoggerFactory.getLogger(str(self.__class__ ))
        pass

    def run(self):
        cfg = SingleConfig.getConfig()
        mqtt = Mqtt.get_instance()
        fgi = Fake_Controller_Interface()
        m_parser = Mqtt.MQTT_Messages_Parser(fgi)

        mqtt.client.on_message=m_parser.parse_message

        while True:
            soil_mositure = fgi.get_soil_moiusture()
            light = fgi.get_light()
            air_temperature = fgi.get_temperature()
            air_moisture = fgi.get_air_moisture()
            
            soil_moisture_guard = int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_MOISTURE_GUARD])

            if soil_mositure <= soil_moisture_guard:
                self.logger.info("start pump, watering for "+cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]+" sec")
                fgi.set_pump_on()
                time.sleep(int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]))
                self.logger.info("stop pump")
                fgi.set_pump_off()

            time.sleep(int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_SLEEP_MIN])*60)

