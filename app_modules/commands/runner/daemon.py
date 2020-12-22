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
import app_modules.core.mqtt as Mqtt
from app_modules.garden_server import Garden_Controller_Interface
import time, json

class Daemon():
    short_arg   = 'D'
    long_arg    = 'daemon'
    cmd_help    = 'Run application in daemon mode, in this mode the \
            application will compare the current soil moisture and if less then\
            treshold it will power on the pump periodically'
    cmd_type    = None
    cmd_action  = 'store_true'

    def __init__(self, param=None):
        pass

    def run(self):
        cfg = SingleConfig.getConfig()
        gci = Garden_Controller_Interface()
        mqtt = Mqtt.get_instance()

        mqtt.client.on_message=parse_message

        while True:
            soil_mositure = gci.get_soil_moiusture()
            light = gci.get_light()
            air_temperature = gci.get_temperature()
            air_moisture = gci.get_air_moisture()
            
            soil_moisture_guard = int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_MOISTURE_GUARD])

            if soil_mositure <= soil_moisture_guard:
                print("start pump, watering for "+cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]+" sec")
                gci.set_pump_on()
                time.sleep(int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC]))
                gci.set_pump_off()
                print("stop pump")

            time.sleep(int(cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_SLEEP_MIN])*60)

def parse_message(client, userdata, message):
    logger = LoggerFactory.getLogger("daemon_parse_message")
    s_message = str(message.payload.decode("utf-8"))

    logger.debug("got message {}".format(s_message))

    try: 
        o_message = json.loads(s_message)
    except:
        logger.warn("message {} cannot be converted to json".format(s_message))
        o_message = {}


    if "id" in o_message:
        if o_message['id'] != SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_DEVICEID]:
            if o_message['tag'] == AppConstants.MQTT_WATERING_CMD_TAG:
                manage_watering_cmd(o_message['value'])
            elif o_message['tag'] == AppConstants.MQTT_AIR_HUMIDITY_TAG:
                pass
            elif o_message['tag'] == AppConstants.MQTT_TEMPERATURE_TAG:
                pass
            elif o_message['tag'] == AppConstants.MQTT_SOIL_MOISTURE_TAG:
                pass
            elif o_message['tag'] == AppConstants.MQTT_LIGHT_TAG_TAG:
                pass
            else:
                logger.debug("message {} has unknown tag: ignored".format(s_message))
        else:
            logger.debug("message {} sent by myself: ignored".format(s_message))
    else:
        logger.warn("message {} is not well formed".format(s_message))

def manage_watering_cmd(value):
    logger = LoggerFactory.getLogger("manage_watering_cmd")
    gci = Garden_Controller_Interface() 
    if value.lower() == 'off':
        gci.set_pump_off()
    elif value.lower() == 'on':
        gci.set_pump_on()
    elif value.lower() == 'status':
        gci.get_pump_status()
    else:
        logger.warn("value {} has is unknown: ignored".format(value))

