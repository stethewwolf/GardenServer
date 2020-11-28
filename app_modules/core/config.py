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
#     The above copyright notice and this permission notice shall be included in all
#     copies or substantial portions of the Software.
# 
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#     SOFTWARE. 

import configparser, os
import app_modules.core.constants as AppConstants

__instance = None

def getConfig():
    global __instance

    if not __instance :
        __instance = configparser.ConfigParser()
        __instance.add_section(AppConstants.CONF_TAG_APP)
        
    return __instance

def loadConfig(path):
    global __instance

    if not __instance:
        getConfig()
    
    if os.path.exists(path):
            __instance.read(path)


def save(cfg):
    with open(AppConstants.CONF_FILE, 'w') as file:
        cfg.write(file)
