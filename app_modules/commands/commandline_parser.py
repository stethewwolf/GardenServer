# File : commandline_parser
# Author : stefano prina 
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

import argparse
import importlib
from app_modules.core import LoggerFactory
from app_modules.core import AppConstants
from app_modules.commands.runner import *
from app_modules.commands.setter import *

class CommandLine_Parser( object ):
    def __init__( self ):
        self.logger = LoggerFactory.getLogger( str( self.__class__ ))

        self.parser = argparse.ArgumentParser( prog=AppConstants.APP_NAME, description=AppConstants.APP_DESCRIPTION )

        self.rcl = [
            Run_version,
            Monitor,
            Pump_On,
            Pump_Off,
            Archive_Data,
            Daemon,
            Daemon_Test
            ]

        self.scl = [
            Set_Baud_Rate,
            Set_Device,
            Set_Time2Water,
            Set_Cicle_Min,
            Set_Mqtt_Server,
            Set_Mqtt_Port
            ]
        # regist set_conf
        self.parser.add_argument(
            "--"+Set_conf.long_arg,
            "-"+Set_conf.short_arg,
            type = Set_conf.cmd_type,
            help = Set_conf.cmd_help
        )

        # register all other cmds
        for cmd in self.rcl + self.scl:
            if cmd.short_arg:
                if cmd.cmd_type:
                    self.parser.add_argument(
                        "--"+cmd.long_arg,
                        "-"+cmd.short_arg,
                        type = cmd.cmd_type,
                        help = cmd.cmd_help
                    )
                else:
                    self.parser.add_argument(
                        "--"+cmd.long_arg,
                        "-"+cmd.short_arg,
                        action = cmd.cmd_action,
                        help = cmd.cmd_help
                    )
            elif cmd.long_arg:
                if cmd.cmd_type:
                    self.parser.add_argument(
                        "--"+cmd.long_arg,
                        type = cmd.cmd_type,
                        help = cmd.cmd_help
                    )
                else:
                    self.parser.add_argument(
                        "--"+cmd.long_arg,
                        action = cmd.cmd_action,
                        help = cmd.cmd_help
                    )

    def parse( self ):
        command_list = []

        # setup application env
        self.logger.debug('add set_env command')
        command_list.append( Set_env() )

        # parse command line
        self.logger.debug('parse start')

        args = self.parser.parse_args()

        # check if conf file is passed
        if getattr( args, Set_conf.long_arg.replace("-","_") ) :
            self.logger.debug("passed option --" + Set_conf.long_arg)
            command_list.append( Set_conf( getattr( args, Set_conf.long_arg.replace("-","_") ) ) )

        for cmd in self.scl:
            if getattr( args, cmd.long_arg.replace("-","_") ) :
                self.logger.debug("passed option --" + cmd.long_arg)
                command_list.append( cmd( getattr( args, cmd.long_arg.replace("-","_") ) ) )

        count = 0
        for cmd in self.rcl:
            if getattr( args, cmd.long_arg.replace("-","_") ) :
                self.logger.debug("passed option --" + cmd.long_arg)
                command_list.append( cmd( getattr( args, cmd.long_arg.replace("-","_") ) ) )
                count += 1

            if count > 1 :
                self.logger.warn("it is possible use only one task")
                break
        
        if count == 0:
            command_list.append(Monitor())


        self.logger.debug('parse ends')
        return command_list
