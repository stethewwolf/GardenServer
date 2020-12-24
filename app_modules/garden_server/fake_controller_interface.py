#!/usr/bin/env python

import random, time 
from app_modules.core import AppDBIface, SingleConfig, AppConstants, LoggerFactory
import app_modules.core.mqtt as mqtt

class Fake_Controller_Interface():
    """ GardenControllerInterface """
    def __init__(self):
        self.dbi = AppDBIface.Database_Interface()
        self.dbi.open()
        self.logger = LoggerFactory.getLogger(str(self.__class__ ))
        self.fake_pump_status = 0

        self.cfg = SingleConfig.getConfig()[AppConstants.CONF_TAG_APP]
        self.device_name = self.cfg[AppConstants.CONF_MQTT_DEVICEID]
        self.mqtts = mqtt.get_instance()

    def get_temperature(self):
        """ get_temperature """
        value = float(random.randint(-5,30)+random.random())

        self.dbi.add_air_temperature(value, self.device_name)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(AppConstants.MQTT_TEMPERATURE_TAG,value)

        return value

    def get_air_moisture(self):
        """ get_air_moisture """
        value = random.random()*100

        self.dbi.add_air_moisture(value, self.device_name)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(AppConstants.MQTT_AIR_HUMIDITY_TAG,value)

        return value

    def get_light(self):
        """ get_light """
        value = float(random.randint(1,101))
        self.dbi.add_light(value, self.device_name)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(AppConstants.MQTT_LIGHT_TAG,value)

        return value

    def get_soil_moiusture(self):
        """ get_soil_moiusture """
        value = float(random.randint(1,101))
        self.dbi.add_soil_moisture(value, self.device_name)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(AppConstants.MQTT_SOIL_MOISTURE_TAG,value)

        return value

    def get_pump_status(self):
        """ get_pump_status """
        value = self.fake_pump_status

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            if value == 1:
                self.mqtts.pub(AppConstants.MQTT_WATERING_TAG,"on")
            elif value == 0:
                self.mqtts.pub(AppConstants.MQTT_WATERING_TAG,"off")
 
        return int(value)

    def set_pump_on(self):
        """ set_pump_on """
        self.fake_pump_status = 1
        value = self.fake_pump_status
        self.dbi.add_pump_status(value, self.device_name)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(AppConstants.MQTT_WATERING_TAG,"on")

    def set_pump_off(self):
        """ set_pump_off """
        self.fake_pump_status = 0
        value = self.fake_pump_status
        self.dbi.add_pump_status(value, self.device_name)

        if self.cfg[AppConstants.CONF_MQTT_ENABLED].lower() == "true" :
            self.mqtts.pub(AppConstants.MQTT_WATERING_TAG,"off")

    def close(self):
        """ close """
        self.dbi.close()



