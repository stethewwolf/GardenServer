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
        SingleConfig.loadConfig
        self.dbi = AppDBIface.get_instance()

    def run( self ):
        # init configuration object
        SingleConfig.loadConfig(CONF_FILE)
        self.cfg = SingleConfig.getConfig()[CONF_TAG_APP]
        self.init_app_conf()

        # manage application folder
        self.home_app_mngr()

        # set up database
        self.dbi.open()

    def init_app_conf(self):
        if CONF_BAUD_RATE  not in self.cfg:
            self.cfg[CONF_BAUD_RATE] = DEFAULT_BAUD_RATE

        if CONF_SERIAL not in self.cfg:
            self.cfg[CONF_SERIAL] = DEFAULT_SERIAL

        if CONF_SLEEP_MIN not in self.cfg:
            self.cfg[CONF_SLEEP_MIN] = DEFAULT_SLEEP_MIN

        if CONF_WATERING_SEC not in self.cfg:
            self.cfg[CONF_WATERING_SEC] = DEFAULT_WATERING_SEC

        if CONF_MOISTURE_GUARD not in self.cfg:
            self.cfg[CONF_MOISTURE_GUARD] = DEFAULT_MOISTURE_GUARD

        if CONF_MQTT_ENABLED not in self.cfg:
            self.cfg[CONF_MQTT_ENABLED] = DEFAULT_MQTT_ENABLED

        if CONF_MQTT_SERVER not in self.cfg:
            self.cfg[CONF_MQTT_SERVER] = DEFAULT_MQTT_SERVER

        if CONF_MQTT_PORT not in self.cfg:
            self.cfg[CONF_MQTT_PORT] = DEFAULT_MQTT_PORT

        if CONF_MQTT_DEVICEID not in self.cfg:
            self.cfg[CONF_MQTT_DEVICEID] = DEFAULT_MQTT_DEVICEID

        if CONF_MQTT_TOPIC not in self.cfg:
            self.cfg[CONF_MQTT_TOPIC] = DEFAULT_MQTT_TOPIC
        
        if CONF_WATERING_ENABLE not in self.cfg:
            self.cfg[CONF_WATERING_ENABLE] = DEFAULT_WATERING_ENABLE
            print("!!!!!!!!!!!!!!!!!!")

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
