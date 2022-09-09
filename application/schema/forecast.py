from datetime import datetime, timedelta
from marshmallow import Schema, fields, EXCLUDE, post_load


class ForecastSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    date = fields.DateTime(data_key="dia", format="%d/%m/%Y", required=True)
    hour = fields.Integer(data_key="hora", required=True)
    city = fields.String(data_key="entidade", required=True)
    state = fields.String(data_key="uf", required=True)
    weather = fields.String(data_key="tempo", required=True)
    summary = fields.String(data_key="resumo")
    max_temp = fields.Integer(data_key="temp_max", required=True)
    max_temp_trend = fields.String(data_key="temp_max_tende", required=True)
    min_temp = fields.Integer(data_key="temp_min", required=True)
    min_temp_trend = fields.String(data_key="temp_min_tende", required=True)
    max_humidity = fields.Integer(data_key="umidade_max", required=True)
    min_humidity = fields.Integer(data_key="umidade_min", required=True)
    wind_direction = fields.String(data_key="dir_vento", required=True)
    wind_speed = fields.String(data_key="int_vento", required=True)
    season = fields.String(data_key="estacao", required=True)
    sunrise = fields.DateTime(data_key="nascer", format="%Hh%M")
    sunset = fields.DateTime(data_key="ocaso", format="%Hh%M")
    source = fields.String(data_key="fonte", required=True)

    @post_load
    def format(self, data: dict, **_):
        date_time = data.pop("date") + timedelta(hours=data.pop('hour'))
        date_time = datetime.fromisoformat(date_time.isoformat() + '-03:00')
        data["date_time"] = date_time

        data['sunrise'] = datetime.fromisoformat(
            data['sunrise'].isoformat() + '-03:00'
        )

        data['sunset'] = datetime.fromisoformat(
            data['sunset'].isoformat() + '-03:00'
        )

        return data


class ForecastQuery(Schema):
    city_id = fields.String(required=True)
    date = fields.DateTime(missing=datetime.now())
    days = fields.Integer(missing=7)
