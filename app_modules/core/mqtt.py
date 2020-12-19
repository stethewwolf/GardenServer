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
from app_modules.core import SingleConfig, AppConstants, LoggerFactory
import time, json

class MQTT_Service(object):
    def __init__(self):
        self.logger = LoggerFactory.getLogger(str(self.__class__ ))
        self.client_id = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_DEVICEID]
        self.brocker_host = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_SERVER]
        self.brocker_port = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP][AppConstants.CONF_MQTT_PORT]
        try:
            self.client = mqtt.Client(self.client_id)
            self.client.enable_logger(self.logger)
            self.client.connect(host=self.brocker_host, port=int(self.brocker_port))

            self.logger.debug("connected with mqtt://{}:{} as {}".format(self.brocker_host, self.brocker_port, self.client_id))
        except :
            self.logger.error("failed to connect with mqtt://{}:{} as {}".format(self.brocker_host,self.brocker_port, self.client_id))

    def pub(self, topic, value):
        o_message = {
            'id' : self.client_id,
            'value': value
        }
        s_message = json.dumps(o_message)

        self.logger.debug("try publish value [{}] on topic [{}]".format(s_message,topic))

        try:
            self.client.publish(topic,s_message)
            time.sleep(1)
            self.logger.debug("published value [{}] on topic [{}]".format(s_message,topic))
        except :
            self.logger.error("failed to publish with mqtt://{}:{}".format(self.brocker_host,self.brocker_port))

    def disconnect(self):
        try:
            self.client.disconnect()
            self.logger.debug("disconnected from mqtt://{}:{}".format(brocker_host,brocker_port))
        except :
            self.logger.error("failed to disconnect from mqtt://{}:{}".format(self.brocker_host,self.brocker_port))


         
