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

import logging, sys

loggerList = {}
logLevel = logging.DEBUG
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = None

def get_handler():
    global handler

    if handler is None:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logLevel)
        handler.setFormatter(formatter)
    
    return handler

def getLogger(name):
    global logLevel
    global loggerList

    if name not in loggerList.values() :
        logger = logging.getLogger(name)
        logger.setLevel(logLevel)
        logger.propagate = False
        logger.addHandler(get_handler())
        loggerList[name] = logger
    else:
        logger = loggerList[name]

    return logger

def setLogFile(file):
    global logLevel
    global loggerList
    handler = logging.StreamHandler(file)
    handler.setLevel(logLevel)
    handler.setFormatter(formatter)

    for l in loggerList.values() :
        l.addHandler(handler)
