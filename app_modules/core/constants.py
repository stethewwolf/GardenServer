# Author : stefano prina 
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
#

import os

APP_NAME                            = 'garden-srv'
APP_DESCRIPTION                     = 'Garden Server app'
APP_VERSION                         = '0.1.0'

APP_HOME = os.path.join(os.environ['HOME'],APP_NAME)
CONF_FILE_NAME = 'conf.ini'
CONF_FILE = os.path.join(APP_HOME, CONF_FILE_NAME)
DB_FILE_NAME = 'data.sqlite'
DB_FILE = os.path.join(APP_HOME, DB_FILE_NAME)

CONF_TAG_APP = 'app'

# min garden controller version supported
CONTROLLER_FW_MIN_VERSION = '11'

CONF_BAUD_RATE = "serial-baud-rate"
DEFAULT_BAUD_RATE = "115200"

CONF_SERIAL = "serial-device"
DEFAULT_SERIAL = "/dev/ttyAMA0"

CONF_SLEEP_MIN = "min2sleep"
DEFAULT_SLEEP_MIN = "15"

CONF_WATERING_SEC = "watering-sec"
DEFAULT_WATERING_SEC = "30"

CONF_MOISTURE_GUARD = "moisture-guard"
DEFAULT_MOISTURE_GUARD = "20"

CONF_MQTT_ENABLED = "mqtt-enabled"
DEFAULT_MQTT_ENABLED = "false"

CONF_MQTT_SERVER = "mqtt-server"
DEFAULT_MQTT_SERVER = "127.0.0.1"

CONF_MQTT_PORT = "mqtt-port"
DEFAULT_MQTT_PORT = "1883"

CONF_MQTT_DEVICEID = "mqtt-device-id"
DEFAULT_MQTT_DEVICEID = "gardenserver"

CONF_MQTT_TOPIC = "garden-topic"
DEFAULT_MQTT_TOPIC = "garden"

MQTT_TEMPERATURE_TAG = "air/temperature"

MQTT_AIR_HUMIDITY_TAG = "air/humidity"

MQTT_SOIL_MOISTURE_TAG = "soil/moisture"

MQTT_LIGHT_TAG = "light"

MQTT_WATERING_TAG = "watering_system/status"

MQTT_GARDEN_CMD_TAG = "cmd"

