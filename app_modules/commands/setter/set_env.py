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
from app_modules.core import AppConstants
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
        self.cfg = SingleConfig.getConfig()
        self.dbi = AppDBIface.get_instance()

    def run( self ):
        # init configuration object
        self.init_app_conf()

        # manage application folder
        self.home_app_mngr()

        # set up database
        self.dbi.open()

    def init_app_conf(self):
        self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_BAUD_RATE] = AppConstants.DEFAULT_BAUD_RATE
        self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_SERIAL] = AppConstants.DEFAULT_SERIAL
        self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_SLEEP_MIN] = AppConstants.DEFAULT_SLEEP_MIN
        self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_WATERING_SEC] = AppConstants.DEFAULT_WATERING_SEC
        self.cfg[AppConstants.CONF_TAG_APP][AppConstants.CONF_MOISTURE_GUARD] = AppConstants.DEFAULT_MOISTURE_GUARD

    def home_app_mngr(self):
        # create app dir inside user home directory
        if not os.path.exists(AppConstants.APP_HOME):
            os.makedirs(AppConstants.APP_HOME)
            self.logger.debug("created app home dir")
        else:
            self.logger.debug("app home dir yet present")

        if not os.path.exists(AppConstants.CONF_FILE):
            SingleConfig.save(self.cfg)
            self.logger.debug("created conf file")
