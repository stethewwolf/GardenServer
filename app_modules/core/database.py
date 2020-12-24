
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
                AUTOINCREMENT, `temperature` FLOAT, `datetime` TEXT, `device_id` INTEGER )'

        self.__DB_CREATE_TABLE_AIR_MOISTURE = 'CREATE TABLE  IF NOT EXISTS `air_moisture` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `moisture` FLOAT, `datetime` TEXT, `device_id` INTEGER )'

        self.__DB_CREATE_TABLE_SOIL_MOISTURE = 'CREATE TABLE  IF NOT EXISTS `soil_moisture` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `moisture` FLOAT, `datetime` TEXT, `device_id` INTEGER )'

        self.__DB_CREATE_TABLE_LIGHT = 'CREATE TABLE  IF NOT EXISTS `light` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `light` FLOAT, `datetime` TEXT, `device_id` INTEGER)'

        self.__DB_CREATE_TABLE_PUMP_STATUS = 'CREATE TABLE  IF NOT EXISTS `pump_status` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `new_status` FLOAT, `datetime` TEXT, `device_id` INTEGER)'

        self.__DB_CREATE_TABLE_DEVICES = 'CREATE TABLE  IF NOT EXISTS `devices` ( `id` INTEGER PRIMARY KEY\
                AUTOINCREMENT, `name` TEXT NOT NULL UNIQUE, `weight` FLOAT DEFAULT 1)'

        self.__DB_INSERT_DEVICE = 'INSERT OR IGNORE INTO `devices` (`name`) VALUES (?);'

        self.__DB_INSERT_APP_TABLE = 'INSERT OR IGNORE INTO `app` (`key`,`value`) VALUES\
                (?,?);'

        self.__DB_INSERT_AIR_TEMPERATURE = 'INSERT INTO `air_temperature`\
                (`temperature`,`datetime`,`device_id`) VALUES (?,?,?);'

        self.__DB_INSERT_AIR_MOISTURE = 'INSERT INTO `air_moisture`\
                (`moisture`,`datetime`,`device_id`) VALUES (?,?,?);'

        self.__DB_INSERT_SOIL_MOISTURE = 'INSERT INTO `soil_moisture`\
                (`moisture`,`datetime`,`device_id`) VALUES (?,?,?);'

        self.__DB_INSERT_LIGHT = 'INSERT INTO `light`\
                (`light`,`datetime`,`device_id`) VALUES (?,?,?);'

        self.__DB_INSERT_PUMP_STATUS = 'INSERT INTO `pump_status`\
                (`new_status`,`datetime`,`device_id`) VALUES (?,?,?);'

        self.__DB_GET_AIR_TEMPERATURE = 'SELECT temperature,datetime,device_id from `air_temperature`\
                WHERE datetime >= ? and datetime<= ?;'

        self.__DB_GET_AIR_TEMPERATURE_BY_DEVICE = 'SELECT temperature,datetime,device_id from `air_temperature`\
                WHERE datetime >= ? and datetime<= ? and device_id==?;'

        self.__DB_GET_AIR_MOISTURE = 'SELECT moisture,datetime,device_id from `air_moisture`\
                WHERE datetime >= ? and datetime<= ?;'

        self.__DB_GET_AIR_MOISTURE_BY_DEVICE = 'SELECT moisture,datetime,device_id from `air_moisture`\
                WHERE datetime >= ? and datetime<= ? and device_id==?;'

        self.__DB_GET_SOIL_MOISTURE = 'SELECT moisture,datetime,device_id from `soil_moisture`\
                WHERE AND datetime >= ? AND datetime<= ?;'

        self.__DB_GET_SOIL_MOISTURE_BY_DEVICE = 'SELECT moisture,datetime,device_id from `soil_moisture`\
                WHERE AND datetime >= ? AND datetime<= ? and device_id==?;'
                
        self.__DB_GET_LIGHT = 'SELECT light,datetime,device_id from `light`\
                WHERE datetime >= ? AND datetime<= ?;'

        self.__DB_GET_LIGHT_BY_DEVICE = 'SELECT light,datetime,device_id from `light`\
                WHERE datetime >= ? AND datetime<= ? and device_id==?;'

        self.__DB_GET_PUMP_STATUS = 'SELECT new_status,datetime,device_id from `pump_status`\
                WHERE datetime >= ? AND datetime<= ?;'

        self.__DB_GET_PUMP_STATUS_BY_DEVICE = 'SELECT new_status,datetime,device_id from `pump_status`\
                WHERE datetime >= ? AND datetime<= ?;'

        self.__DB_GET_DEVICE_ID = 'SELECT id,name,weight from `devices`\
                WHERE id == ?;'

        self.__DB_GET_DEVICE_NAME = 'SELECT id,name,weight from `devices`\
                WHERE name == ?;'


        self.con = None

    def open(self):
        # open db 
        self.con = sqlite3.connect(AppConstants.DB_FILE)

        #  check db contain tables
        cursor = self.con.cursor()
        cursor.execute(self.__DB_CREATE_TABLE_APP)
        cursor.execute(self.__DB_CREATE_TABLE_AIR_TEMPERATURE)
        cursor.execute(self.__DB_CREATE_TABLE_AIR_MOISTURE)
        cursor.execute(self.__DB_CREATE_TABLE_SOIL_MOISTURE)
        cursor.execute(self.__DB_CREATE_TABLE_LIGHT)
        cursor.execute(self.__DB_CREATE_TABLE_PUMP_STATUS)
        cursor.execute(self.__DB_CREATE_TABLE_DEVICES)
        cursor.execute(self.__DB_INSERT_APP_TABLE,("app_version",AppConstants.APP_VERSION))
        #cursor.execute(self.__DB_INSERT_APP_TABLE,("fw_min_version",AppConstants.CONTROLLER_FW_MIN_VERSION))
        self.con.commit()

    def add_device(self, device_name):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_INSERT_DEVICE, [device_name])
        self.con.commit()

        return self.get_device_by_name(device_name)

    def get_device_by_id(self, id):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_GET_DEVICE_ID, [id])
        row = cursor.fetchone()

        if row is not None:
            return {
                'id': row[0],
                'name': row[1],
                'weight' : row[1]
            }
        else:
            return None

    def get_device_by_name(self, name):
        cursor = self.con.cursor()
        cursor.execute(self.__DB_GET_DEVICE_NAME, [name])
        row = cursor.fetchone()
        if row is not None:
            return {
                'id': row[0],
                'name': row[1],
                'weight' : row[1]
            }
        else:
            return None

    def add_air_temperature(self, value, device_name):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()

        d_device = self.get_device_by_name(device_name)

        if d_device is None:
            d_device = self.add_device(device_name)

        cursor.execute(self.__DB_INSERT_AIR_TEMPERATURE, (value, timestamp, d_device['id']))
        self.con.commit()

    def get_air_temperature(self, start_datetime=datetime.datetime.now()-datetime.timedelta(hours=24),\
                            end_datetime=datetime.datetime.now(), device_name=None):
        cursor = self.con.cursor()

        if device_name is None:
            cursor.execute(self.__DB_GET_AIR_TEMPERATURE, (start_datetime,end_datetime))
        else:
            d_device = self.get_device_by_name(device_name)
            cursor.execute(self.__DB_GET_AIR_TEMPERATURE_BY_DEVICE, (start_datetime,end_datetime,d_device['id']))

        return [ {'value':float(row[0]),'time':datetime.datetime(row[1]),'device':row[2]} for row in cursor.fetchall()]

    def add_air_moisture(self, value, device_name):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        d_device = self.get_device_by_name(device_name)

        if d_device is None:
            d_device = self.add_device(device_name)

        cursor.execute(self.__DB_INSERT_AIR_MOISTURE, (value, timestamp, d_device['id']))
        self.con.commit()

    def get_air_moisture(self, start_datetime=datetime.datetime.now()-datetime.timedelta(hours=24),\
                            end_datetime=datetime.datetime.now(), device_name=None):
        cursor = self.con.cursor()

        if device_name is None:
            cursor.execute(self.__DB_GET_AIR_MOISTURE, (start_datetime,end_datetime))
        else:
            d_device = self.get_device_by_name(device_name)
            cursor.execute(self.__DB_GET_AIR_MOISTURE_BY_DEVICE, (start_datetime,end_datetime, d_device['id']))

        return [ {'value':float(row[0]),'time':datetime.datetime(row[1]),'device':row[2]} for row in cursor.fetchall()]

    def add_soil_moisture(self, value, device_name):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        d_device = self.get_device_by_name(device_name)

        if d_device is None:
            d_device = self.add_device(device_name)

        cursor.execute(self.__DB_INSERT_SOIL_MOISTURE, (value, timestamp, d_device['id']))
 
        self.con.commit()

    def get_soil_moisture(self, start_datetime=datetime.datetime.now()-datetime.timedelta(hours=24),\
                            end_datetime=datetime.datetime.now(), device_name=None):
        cursor = self.con.cursor()

        if device_name is None:
            cursor.execute(self.__DB_GET_SOIL_MOISTURE, (start_datetime,end_datetime))
        else:
            d_device = self.get_device_by_name(device_name)
            cursor.execute(self.__DB_GET_AIR_MOISTURE_BY_DEVICE, (start_datetime,end_datetime, d_device['id']))

        return [ {'value':float(row[0]),'time':datetime.datetime(row[1]),'device':row[2]} for row in cursor.fetchall()]

    def add_light(self, value, device_name):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        d_device = self.get_device_by_name(device_name)

        if d_device is None:
            d_device = self.add_device(device_name)

        cursor.execute(self.__DB_INSERT_LIGHT, (value, timestamp, d_device['id']))
 
        self.con.commit()

    def get_light(self, start_datetime=datetime.datetime.now()-datetime.timedelta(hours=24),\
                            end_datetime=datetime.datetime.now()):
        cursor = self.con.cursor()
        if device_name is None:
            cursor.execute(self.__DB_GET_LIGHT, (start_datetime,end_datetime))
        else:
            d_device = self.get_device_by_name(device_name)
            cursor.execute(self.__DB_GET_LIGHT_BY_DEVICE, (start_datetime,end_datetime, d_device['id']))

        return [ {'value':float(row[0]),'time':datetime.datetime(row[1]),'device':row[2]} for row in cursor.fetchall()]

    def add_pump_status(self, value, device_name):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        d_device = self.get_device_by_name(device_name)

        if d_device is None:
            d_device = self.add_device(device_name)

        cursor.execute(self.__DB_INSERT_PUMP_STATUS, (value, timestamp, d_device['id']))
 
        self.con.commit()

    def get_pump_status(self, start_datetime=datetime.datetime.now()-datetime.timedelta(hours=24),\
                            end_datetime=datetime.datetime.now()):
        cursor = self.con.cursor()
        
        if device_name is None:
            cursor.execute(self.__DB_GET_PUMP_STATUS, (start_datetime,end_datetime))
        else:
            d_device = self.get_device_by_name(device_name)
            cursor.execute(self.__DB_GET_PUMP_STATUS_BY_DEVICE, (start_datetime,end_datetime, d_device['id']))

        return [ {'value':int(row[0]),'time':datetime.datetime(row[1]),'device':row[2]} for row in cursor.fetchall()]

    def close(self):
        self.con.close()

