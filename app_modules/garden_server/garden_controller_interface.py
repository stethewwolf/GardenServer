#!/usr/bin/env python

import serial, time
from app_modules.core import AppDBIface

class Garden_Controller_Interface():
    """ GardenControllerInterface """
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', '9600')
        self.dbi = AppDBIface.get_instance()

        self.commands_map = {'air_temp':'0', 'air_moisture':'1',
                             'light':'2', 'pump_statu':'3', 'pump_on':'4',
                             'pump_off':'5', 'soil_moisture_1':'6',
                             'soil_moisture_2':'7', 'fw_version':'8'}
        # TODO: add fw compatibility check

    def get_temperature(self):
        """ get_temperature """
        self.ser.write(self.commands_map['air_temp'].encode())
        time.sleep(1)
        value = float(self.ser.readline().decode())
        self.dbi.add_air_temperature(value)
        return value

    def get_air_moisture(self):
        """ get_air_moisture """
        self.ser.write(self.commands_map['air_moisture'].encode())
        time.sleep(1)
        value = float(self.ser.readline().decode())
        self.dbi.add_air_moisture(value)
        return value

    def get_light(self):
        """ get_light """
        self.ser.write(self.commands_map['light'].encode())
        time.sleep(1)
        value = float(self.ser.readline())
        value = value.decode()
        self.dbi.add_light(value)
        return value

    def get_soil_moiusture(self, sensor_idx):
        """ get_soil_moiusture """
        flag = False
        if sensor_idx == 1:
            self.ser.write(self.commands_map['soil_moisture_1'].encode())
            flag = True
        elif sensor_idx == 2:
            self.ser.write(self.commands_map['soil_moisture_2'].encode())
            flag = True

        time.sleep(1)
        value = 0
        if flag:
            value = float(self.ser.readline())
            value = value.decode()
        self.dbi.add_soil_moisture(sensor_idx,value)
        return value

    def get_pump_status(self):
        """ get_pump_status """
        self.ser.write(self.commands_map['pump_status'].encode())
        time.sleep(1)
        value = self.ser.readline()
        return float(value.decode())

    def set_pump_on(self):
        """ set_pump_on """
        self.ser.write(self.commands_map['pump_on'].encode())
        time.sleep(1)
        value = self.ser.readline()
        self.dbi.add_pump_status(value.decode())

    def set_pump_off(self):
        """ set_pump_off """
        self.ser.write(self.commands_map['pump_off'].encode())
        value = self.ser.readline()
        time.sleep(1)
        self.dbi.add_pump_status(value.decode())

    def close(self):
        """ close """
        self.ser.close()



