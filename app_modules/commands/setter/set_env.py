#
#   Author : stefano prina <stethewwolf@null.net>
#
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
from app_modules.core.constants import *
from app_modules.commands.command import Command
from app_modules.core import AppDBIface

import os, sqlite3

class Set_env( Command ):
    short_arg   = None
    long_arg    = None
    cmd_help    = None
    cmd_type    = None
    cmd_action  = None

    def __init__( self, param  = None ):
        super().__init__( )
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))
        self.cfg = SingleConfig.getConfig()[CONF_TAG_APP]
        self.dbi = AppDBIface.get_instance()

    def run( self ):
        # init configuration object
        self.init_app_conf()

        # manage application folder
        self.home_app_mngr()

        # set up database
        self.dbi.open()

    def init_app_conf(self):
        self.cfg[CONF_BAUD_RATE] = DEFAULT_BAUD_RATE
        self.cfg[CONF_SERIAL] = DEFAULT_SERIAL
        self.cfg[CONF_SLEEP_MIN] = DEFAULT_SLEEP_MIN
        self.cfg[CONF_WATERING_SEC] = DEFAULT_WATERING_SEC
        self.cfg[CONF_MOISTURE_GUARD] = DEFAULT_MOISTURE_GUARD
        self.cfg[CONF_MQTT_ENABLED] = DEFAULT_MQTT_ENABLED
        self.cfg[CONF_MQTT_SERVER] = DEFAULT_MQTT_SERVER
        self.cfg[CONF_MQTT_PORT] = DEFAULT_MQTT_PORT
        self.cfg[CONF_MQTT_DEVICEID] = DEFAULT_MQTT_DEVICEID
        self.cfg[CONF_MQTT_TEMPERATURE_TOPIC] = DEFAULT_MQTT_TEMPERATURE_TOPIC
        self.cfg[CONF_MQTT_AIR_HUMIDITY_TOPIC] = DEFAULT_MQTT_AIR_HUMIDITY_TOPIC
        self.cfg[CONF_MQTT_SOIL_MOISTURE_TOPIC] = DEFAULT_MQTT_SOIL_MOISTURE_TOPIC
        self.cfg[CONF_MQTT_LIGHT_TOPIC] = DEFAULT_MQTT_LIGHT_TOPIC

    def home_app_mngr(self):
        # create app dir inside user home directory
        if not os.path.exists(APP_HOME):
            os.makedirs(APP_HOME)
            self.logger.debug("created app home dir")
        else:
            self.logger.debug("app home dir yet present")

        if not os.path.exists(CONF_FILE):
            SingleConfig.save(SingleConfig.getConfig())
            self.logger.debug("created conf file")
