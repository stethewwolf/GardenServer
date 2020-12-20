#!/usr/bin/env python

import serial, time
from app_modules.core import AppDBIface, SingleConfig, AppConstants, LoggerFactory
from app_modules.core.mqtt import MQTT_Service

class Garden_Controller_Interface():
    """ GardenControllerInterface """
    def __init__(self):
        self.commands_map = {'air_temp':'0\n', 'air_moisture':'1\n',
                             'light':'2\n', 'pump_status':'3\n', 'pump_on':'4\n',
                             'pump_off':'5\n', 'soil_moisture':'6\n',
                             'fw_version':'7\n'}
        self.dbi = AppDBIface.get_instance()
        self.logger = LoggerFactory.getLogger(str(self.__class__ ))

        self.cfg = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP]
        device = self.cfg[AppConstants.CONF_SERIAL]
        baud_rate = self.cfg[AppConstants.CONF_BAUD_RATE]
        self.mqtts = MQTT_Service()

        self.sec2sleep = 1

        self.ser = serial.Serial(device, baud_rate)
        self.logger.debug("opened serial device : "+device+" with baud rate : "+baud_rate)

        # waith until device is not ready
        fw_ver = -1
        while fw_ver < 0:
            fw_ver = self.get_fw_version()

        # compatibility check
        if not self.check_fw():
            self.logger.error("Controller version not supported, please update and try again")
            raise Exception("Controller version not supported, please update and try again")


    def check_fw(self):
        check = False
        min_supported_version = AppConstants.CONTROLLER_FW_MIN_VERSION
        self.logger.debug("min controller version supported " + min_supported_version )

        if int(min_supported_version) < self.get_fw_version():
            check = True

        self.logger.debug("controller version " + str(self.get_fw_version()))

        return check

    def get_fw_version(self):
        """ get_temperature """
        self.ser.write(self.commands_map['fw_version'].encode())
        time.sleep(self.sec2sleep)

        value = self.ser.readline()
        value = int(value.decode())
        self.dbi.add_air_temperature(value)
        return value

    def get_temperature(self):
        """ get_temperature """
        self.ser.write(self.commands_map['air_temp'].encode())
        time.sleep(self.sec2sleep)

        value = self.ser.readline()
        value = float(value.decode())
        self.dbi.add_air_temperature(value)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(self.cfg[AppConstants.CONF_MQTT_TEMPERATURE_TAG],value)

        return value

    def get_air_moisture(self):
        """ get_air_moisture """
        self.ser.write(self.commands_map['air_moisture'].encode())
        time.sleep(self.sec2sleep)

        value = self.ser.readline()
        value = float(value.decode())
        self.dbi.add_air_moisture(value)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(self.cfg[AppConstants.CONF_MQTT_AIR_HUMIDITY_TAG],value)

        return value

    def get_light(self):
        """ get_light """
        self.ser.write(self.commands_map['light'].encode())
        time.sleep(self.sec2sleep)

        value = self.ser.readline()
        value = float(value.decode())
        self.dbi.add_light(value)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(self.cfg[AppConstants.CONF_MQTT_LIGHT_TAG],value)

        return value

    def get_soil_moiusture(self):
        """ get_soil_moiusture """
        
        self.ser.write(self.commands_map['soil_moisture'].encode())
        time.sleep(self.sec2sleep)

        value = 0
        value = self.ser.readline()
        value = float(value.decode())
        self.dbi.add_soil_moisture(value)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(self.cfg[AppConstants.CONF_MQTT_SOIL_MOISTURE_TAG],value)

        return value

    def get_pump_status(self):
        """ get_pump_status """
        self.ser.write(self.commands_map['pump_status'].encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        return int(value.decode())

    def set_pump_on(self):
        """ set_pump_on """
        self.ser.write(self.commands_map['pump_on'].encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        self.dbi.add_pump_status(value.decode())

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(self.cfg[AppConstants.CONF_MQTT_WATERING_TAG],"on")

    def set_pump_off(self):
        """ set_pump_off """
        self.ser.write(self.commands_map['pump_off'].encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        self.dbi.add_pump_status(value.decode())

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(self.cfg[AppConstants.CONF_MQTT_WATERING_TAG],"off")

    def close(self):
        """ close """
        self.ser.close()



