
import sqlite3, datetime
from app_modules.core import SingleConfig
from app_modules.core import AppConstants

__instance = None

def get_instance():
    global __instance

    if not __instance:
        __instance = Database_Interface()

    return __instance

class Database_Interface():
    def __init__(self):
        self.__DB_CREATE_TABLE_APP = 'CREATE TABLE IF NOT EXISTS `app` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `key` TEXT UNIQUE, `value` TEXT )'
        self.__DB_CREATE_TABLE_AIR_TEMPERATURE = 'CREATE TABLE  IF NOT EXISTS `air_temperature` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `temperature` FLOAT, `datetime` TEXT )'
        self.__DB_CREATE_TABLE_AIR_MOISTURE = 'CREATE TABLE  IF NOT EXISTS `air_moisture` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `moisture` FLOAT, `datetime` TEXT )'
        self.__DB_CREATE_TABLE_SOIL_MOISTURE = 'CREATE TABLE  IF NOT EXISTS `soil_moisture` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `moisture` FLOAT, `datetime` TEXT, `sensor_id` INTEGER  )'
        self.__DB_CREATE_TABLE_LIGHT = 'CREATE TABLE  IF NOT EXISTS `light` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `light` FLOAT, `datetime` TEXT )'
        self.__DB_CREATE_TABLE_PUMP_STATUS = 'CREATE TABLE  IF NOT EXISTS `pump_status` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `new_status` FLOAT, `datetime` TEXT)'
        self.__DB_INSERT_APP_TABLE = 'INSERT OR IGNORE INTO `app` (`key`,`value`) VALUES\
                (?,?);'
        self.__DB_INSERT_AIR_TEMPERATURE = 'INSERT INTO `air_temperature`\
                (`temperature`,`datetime`) VALUES (?,?);'
        self.__DB_INSERT_AIR_MOISTURE = 'INSERT INTO `air_moisture`\
                (`moisture`,`datetime`) VALUES (?,?);'
        self.__DB_INSERT_SOIL_MOISTURE = 'INSERT INTO `soil_moisture`\
                (`sensor_id`, `moisture`,`datetime`) VALUES (?,?,?);'
        self.__DB_INSERT_LIGHT = 'INSERT INTO `light`\
                (`light`,`datetime`) VALUES (?,?);'
        self.__DB_INSERT_PUMP_STATUS = 'INSERT INTO `pump_status`\
                (`new_status`,`datetime`) VALUES (?,?);'
        self.__DB_GET_AIR_TEMPERATURE = 'SELECT temperature,datetime from `air_temperature`\
                WHERE datetime >= ? and datetime<= ?;'
        self.__DB_GET_AIR_MOISTURE = 'SELECT moisture,datetime from `air_moisture`\
                WHERE datetime >= ? and datetime<= ?;'
        self.__DB_GET_SOIL_MOISTURE = 'SELECT moisture,datetime from `soil_moisture`\
                WHERE sensor_id == ? AND datetime >= ? AND datetime<= ?;'
        self.__DB_GET_LIGHT = 'SELECT light,datetime from `light`\
                WHERE datetime >= ? AND datetime<= ?;'
        self.__DB_GET_PUMP_STATUS = 'SELECT new_status,datetime from `pump_status`\
                WHERE datetime >= ? AND datetime<= ?;'

        self.con = None

    def open(self):
        # open db 
        self.con = sqlite3.connect(SingleConfig.getConfig()['private']['data'])

        #  check db contain tables
        cursor = self.con.cursor()
        cursor.execute(self.__DB_CREATE_TABLE_APP)
        cursor.execute(self.__DB_CREATE_TABLE_AIR_TEMPERATURE)
        cursor.execute(self.__DB_CREATE_TABLE_AIR_MOISTURE)
        cursor.execute(self.__DB_CREATE_TABLE_SOIL_MOISTURE)
        cursor.execute(self.__DB_CREATE_TABLE_LIGHT)
        cursor.execute(self.__DB_CREATE_TABLE_PUMP_STATUS)
        #cursor.execute(self.__DB_INSERT_APP_TABLE,("app_version",AppConstants.APP_VERSION))
        #cursor.execute(self.__DB_INSERT_APP_TABLE,("fw_min_version",AppConstants.CONTROLLER_FW_MIN_VERSION))
        self.con.commit()

    def add_air_temperature(self, value):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        cursor.execute(self.__DB_INSERT_AIR_TEMPERATURE, (value, timestamp))
        self.con.commit()

    def get_air_temperature(self, start_datetime=datetime.datetime.now(),\
                            end_datetime=datetime.datetime.now()):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_GET_AIR_TEMPERATURE, (start_datetime,end_datetime))

        return [ (float(row[0]),datetime.datetime(row[1])) for row in cursor.fetchall()]

    def add_air_moisture(self, value):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        cursor.execute(self.__DB_INSERT_AIR_MOISTURE, (value, timestamp))
        self.con.commit()

    def get_air_moisture(self, start_datetime=datetime.datetime.now(),\
                            end_datetime=datetime.datetime.now()):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_GET_AIR_MOISTURE, (start_datetime,end_datetime))

        return [ (float(row[0]),datetime.datetime(row[1])) for row in cursor.fetchall()]

    def add_soil_moisture(self, sensor_id, value):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        cursor.execute(self.__DB_INSERT_SOIL_MOISTURE, (sensor_id, value,\
                                                   timestamp))
        self.con.commit()

    def get_soil_moisture(self, sensor_id, start_datetime=datetime.datetime.now(),\
                            end_datetime=datetime.datetime.now()):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_GET_SOIL_MOISTURE, (sensor_id,start_datetime,end_datetime))

        return [ (float(row[0]),datetime.datetime(row[1])) for row in cursor.fetchall()]

    def add_light(self, value):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        cursor.execute(self.__DB_INSERT_LIGHT, (value, timestamp))
        self.con.commit()

    def get_light(self, start_datetime=datetime.datetime.now(),\
                            end_datetime=datetime.datetime.now()):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_GET_AIR_MOISTURE, (start_datetime,end_datetime))

        return [ (float(row[0]),datetime.datetime(row[1])) for row in cursor.fetchall()]

    def add_pump_status(self, value):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        cursor.execute(self.__DB_INSERT_PUMP_STATUS, (value, timestamp))
        self.con.commit()

    def get_pump_status(self, start_datetime=datetime.datetime.now(),\
                            end_datetime=datetime.datetime.now()):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_GET_PUMP_STATUS, (start_datetime,end_datetime))

        return [ (int(row[0]),datetime.datetime(row[1])) for row in cursor.fetchall()]

    def close(self):
        self.con.close()

