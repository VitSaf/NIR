import re
from typing import NamedTuple

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '192.168.0.8'
INFLUXDB_USER = 'user'
INFLUXDB_PASSWORD = 'pass'
INFLUXDB_DATABASE = 'DB'

#подключение
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)


class SensorData(NamedTuple):
    location: str
    measurement: str
    value: float

#пример добавления данных
def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'location': sensor_data.location
            },
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    influxdb_client.write_points(json_body)

#инициация бд
def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

#пример селекта
def get_data_by_query():
	return client.query('SELECT "duration" FROM "pyexample"."autogen"."brushEvents" WHERE time > now() - 4d GROUP BY "user"')


_init_influxdb_database()
