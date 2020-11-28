#!/usr/bin/env python

import serial, time
from app_modules.core import AppDBIface

class Garden_Controller_Interface():
    """ GardenControllerInterface """
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', '115200')
        self.dbi = AppDBIface.get_instance()

        self.commands_map = {'air_temp':'0', 'air_moisture':'1',
                             'light':'2', 'pump_status':'3', 'pump_on':'4',
                             'pump_off':'5', 'soil_moisture_1':'6',
                             'soil_moisture_2':'7', 'fw_version':'8'}
        self.sec2sleep = 2
        # TODO: add fw compatibility check

    def get_temperature(self):
        """ get_temperature """
        self.ser.write(self.commands_map['air_temp'].encode())
        #self.ser.write('\n'.encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        value = float(value.decode())
        #self.dbi.add_air_temperature(value)
        return value

    def get_air_moisture(self):
        """ get_air_moisture """
        self.ser.write(self.commands_map['air_moisture'].encode())
        #self.ser.write('\n'.encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        value = float(value.decode())
        #self.dbi.add_air_moisture(value)
        return value

    def get_light(self):
        """ get_light """
        self.ser.write(self.commands_map['light'].encode())
        #self.ser.write('\n'.encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        value = float(value.decode())
        #self.dbi.add_light(value)
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
        #self.ser.write('\n'.encode())

        time.sleep(self.sec2sleep)

        value = 0
        if flag:
            value = self.ser.readline()
            value = float(value.decode())
        #self.dbi.add_soil_moisture(sensor_idx,value)
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
        #self.ser.write('\n'.encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        #self.dbi.add_pump_status(value.decode())


    def set_pump_off(self):
        """ set_pump_off """
        self.ser.write(self.commands_map['pump_off'].encode())
        #self.ser.write('\n'.encode())
        time.sleep(self.sec2sleep)
        value = self.ser.readline()
        #self.dbi.add_pump_status(value.decode())


    def close(self):
        """ close """
        self.ser.close()



