# Author : stefano prina
#
# MIT License
#
# Copyright (c) 2017 Stefano Prina <stethewwolf@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without sestriction, including without limitation the rights
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

import paho.mqtt.client as mqtt
from app_modules.core import SingleConfig, AppConstants, LoggerFactory, AppDBIface
import time, json

__instance = None

def parse_message(client, userdata, message):
    logger = LoggerFactory.getLogger("default_parse_message")
    s_message = str(message.payload.decode("utf-8"))

    logger.warn("got message {}".format(s_message))

def get_instance():
    global __instance

    if __instance is None:
        __instance = MQTT_Service()
    
    return __instance

class MQTT_Service(object):
    def __init__(self):
        self.logger = LoggerFactory.getLogger(str(self.__class__ ))
        self.client_id = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_DEVICEID]
        self.brocker_host = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_SERVER]
        self.brocker_port = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_PORT]
        self.topic = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_TOPIC]

        try:
            self.client = mqtt.Client(self.client_id)
            self.client.enable_logger(self.logger)

            self.client.on_message = parse_message
            
            self.client.connect(host=self.brocker_host, port=int(self.brocker_port))
            self.client.subscribe(self.topic+"/#",0)
            self.client.loop_start()

            self.logger.debug("connected with mqtt://{}:{} as {}".format(self.brocker_host, self.brocker_port, self.client_id))
        except :
            self.logger.error("failed to connect with mqtt://{}:{} as {}".format(self.brocker_host,self.brocker_port, self.client_id))

    def pub(self, tag, value):
        o_message = {
            'id' : self.client_id,
            'value': value,
            'tag' : tag
        }
        s_message = json.dumps(o_message)

        self.logger.debug("try publish value [{}] on topic [{}]".format(s_message,self.topic))

        try:
            self.client.publish("{}/{}".format(self.topic,tag),s_message)
            time.sleep(1)
            self.logger.debug("published value [{}] on topic [{}]".format(s_message,self.topic))
        except :
            self.logger.error("failed to publish with mqtt://{}:{}".format(self.brocker_host,self.brocker_port))

    def disconnect(self):
        try:
            self.client.disconnect()
            self.logger.debug("disconnected from mqtt://{}:{}".format(brocker_host,brocker_port))
        except :
            self.logger.error("failed to disconnect from mqtt://{}:{}".format(self.brocker_host,self.brocker_port))

         
class MQTT_Messages_Parser(object):
    def __init__(self, garden_controller_interface):
        self.gci = garden_controller_interface
        self.logger = LoggerFactory.getLogger(str(self.__class__ ))

    def parse_message(self, client, userdata, message):
        s_message = str(message.payload.decode("utf-8"))

        self.logger.debug("got message {}".format(s_message))

        try: 
            o_message = json.loads(s_message)
        except:
            self.logger.warn("message {} cannot be converted to json".format(s_message))
            o_message = {}


        if "id" in o_message:
            dbi = AppDBIface.Database_Interface()
            dbi.open()
 
            if o_message['id'] != SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_DEVICEID]:
                if o_message['tag'] == AppConstants.MQTT_GARDEN_CMD_TAG:
                    self.manage_cmd(o_message['value'])
                elif o_message['tag'] == AppConstants.MQTT_AIR_HUMIDITY_TAG:
                    dbi.add_air_moisture(o_message['value'],o_message['id'])
                elif o_message['tag'] == AppConstants.MQTT_TEMPERATURE_TAG:
                    dbi.add_air_temperature(o_message['value'],o_message['id'])
                elif o_message['tag'] == AppConstants.MQTT_SOIL_MOISTURE_TAG:
                    dbi.add_soil_moisture(o_message['value'],o_message['id'])
                elif o_message['tag'] == AppConstants.MQTT_LIGHT_TAG:
                    dbi.add_light(o_message['value'],o_message['id'])
                else:
                    self.logger.debug("message {} has unknown tag: ignored".format(s_message))
            else:
                self.logger.debug("message {} sent by myself: ignored".format(s_message))
            dbi.close()
        else:
            self.logger.warn("message {} is not well formed".format(s_message))

    def manage_cmd(self, value):
        if value.lower() == 'water_off':
            self.gci.set_pump_off()
        elif value.lower() == 'water_on':
            self.gci.set_pump_on()
        elif value.lower() == 'water_status':
            self.gci.get_pump_status()
        else:
            self.logger.warn("value {} has is unknown: ignored".format(value))

