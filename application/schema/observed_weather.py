from marshmallow import Schema, fields, post_load
from datetime import datetime as dt


class ObservedWeatherSchema(Schema):
    # Station
    station_code = fields.String(required=True)
    name = fields.String(required=True)
    status = fields.String(missing=None)
    type = fields.String(missing=None)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    altitude = fields.Float(missing=None)
    start_operation = fields.DateTime(missing=None)
    end_operation = fields.DateTime(missing=None)
    source = fields.String(missing='unknown')

    # Observed data
    msr_date = fields.DateTime('%Y-%m-%d', required=True)
    msr_hour = fields.Time('%H%M', required=True)
    temp = fields.Float(missing=None)
    min_temp = fields.Float(missing=None)
    max_temp = fields.Float(missing=None)
    avg_temp = fields.Float(missing=None)
    insolation = fields.Float(missing=None)
    cloudiness = fields.Float(missing=None)
    humidity = fields.Float(missing=None)
    avg_humidity = fields.Float(missing=None)
    rain = fields.Float(missing=None)
    wind_speed = fields.Float(missing=None)
    wind_direction = fields.Float(missing=None)
    gust = fields.Float(missing=None)
    pressure = fields.Float(missing=None)

    @post_load
    def format(self, data: dict, **kwargs):
        station = {
            'code': data['station_code'],
            'name': data['name'],
            'status': data['status'],
            'type': data['type'],
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'altitude': data['altitude'],
            'start_operation': data['start_operation'],
            'end_operation': data['end_operation'],
            'source': data['source'],
        }
        observed_data = {
            'measurement_date': dt.combine(data['msr_date'], data['msr_hour']),
            'temp': data['temp'],
            'min_temp': data['min_temp'],
            'max_temp': data['max_temp'],
            'avg_temp': data['avg_temp'],
            'insolation': data['insolation'],
            'cloudiness': data['cloudiness'],
            'humidity': data['humidity'],
            'avg_humidity': data['avg_humidity'],
            'rain': data['rain'],
            'wind_speed': data['wind_speed'],
            'wind_direction': data['wind_direction'],
            'gust': data['gust'],
            'pressure': data['pressure'],
        }

        return station, observed_data


class ObservedWeatherQuerySchema(Schema):
    station_id = fields.String(required=True)
    start = fields.DateTime(format='%Y-%m-%d')
    end = fields.DateTime(format='%Y-%m-%d')
