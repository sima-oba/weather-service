from marshmallow import Schema, fields, post_load


class RainfallSchema(Schema):
    date_time = fields.DateTime(required=True)
    code = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    latitude = fields.Float()
    longitude = fields.Float()
    altitude = fields.Float()
    total_rainfall = fields.Float(missing=None)
    atmospheric_pressure_at_station_level = fields.Float(required=True)
    atmospheric_pressure_maximum = fields.Float(required=True)
    atmospheric_pressure_minimum = fields.Float(required=True)
    global_radiation = fields.Float(missing=None)
    temp_dry_bulb = fields.Float(required=True)
    temp_maximum = fields.Float(required=True)
    temp_minimum = fields.Float(required=True)
    temp_dew_point = fields.Float(required=True)
    temp_dew_maximum = fields.Float(required=True)
    temp_dew_minimum = fields.Float(required=True)
    humidity_air = fields.Float(required=True)
    humidity_maximum = fields.Float(required=True)
    humidity_minimum = fields.Float(required=True)
    wind_clockwise_direction = fields.Float(required=True)
    wind_speed = fields.Float(missing=None)
    wind_gust_maximum = fields.Float(required=True)

    @post_load
    def format(self, data: dict, **_) -> dict:
        station = {
            'code': data['code'],
            'city': data['city'],
            'state': data['state'],
            'altitude': data['altitude'],
            'geometry': {
                'type': 'Point',
                'coordinates': [data['longitude'], data['latitude']],
            },
        }

        measurement = {
            'date_time': data['date_time'],
            'total_rainfall': data['total_rainfall'],
            'atmospheric_pressure': {
                'at_station_level': data[
                    'atmospheric_pressure_at_station_level'
                ],
                'maximum': data['atmospheric_pressure_maximum'],
                'minimum': data['atmospheric_pressure_minimum'],
            },
            'global_radiation': data['global_radiation'],
            'temperature': {
                'dry_bulb': data['temp_dry_bulb'],
                'maximum': data['temp_maximum'],
                'minimum': data['temp_minimum'],
                'dew_point': data['temp_dew_point'],
                'dew_maximum': data['temp_dew_maximum'],
                'dew_minimum': data['temp_dew_minimum'],
            },
            'humidity': {
                'air': data['humidity_air'],
                'maximum': data['humidity_maximum'],
                'minimum': data['humidity_minimum'],
            },
            'wind': {
                'clockwise_direction': data['wind_clockwise_direction'],
                'speed': data['wind_speed'],
                'gust_maximum': data['wind_gust_maximum'],
            },
        }

        return {'station': station, 'measurement': measurement}


class RainfallQuery(Schema):
    day = fields.Date(required=True)
