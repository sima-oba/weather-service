from uuid import uuid4
import pytest
from datetime import datetime, timedelta, timezone
from application import rest
from domain.entity.geometry import Geometry
from domain.entity.rainfall_measurement import (
    AtmosphericPressure,
    Humidity,
    RainfallMeasurement,
    Temperature,
    Wind
)
from domain.entity.rainfall_station import RainfallStation
from infrastructure import database
from . import TestConfig as config

API_PREFIX = rest.server.URL_PREFIX


def now():
    tzobj = timezone(timedelta(0), name="UTC")
    return datetime.utcnow().replace(second=0, microsecond=0, tzinfo=tzobj)


@pytest.fixture
def clientinstance():
    app = rest.server.create_server(config)
    return app.test_client()


@pytest.fixture(autouse=True)
def db():
    db = database.get_database(config.MONGODB_SETTINGS)

    for collection in db.collection_names(False):
        db.drop_collection(collection)

    return db


@pytest.fixture
def city_entry(db):
    collection = db['city']

    expected = [
        {
            '_id': str(uuid4()),
            'created_at': None,
            'updated_at': None,
            'geoid': '1600303',
            'name': 'Macapá',
            'state': 'AP'
        }
    ]

    collection.insert_many(expected)
    return expected


@pytest.fixture
def ws_entry(db):
    collection = db['station']

    expected = {
        "_id": str(uuid4()),
        "code": str(uuid4()),
        'created_at': None,
        'updated_at': None,
        'name': "Test Station",
        'status': "Online",
        'type': "",
        'latitude': "",
        'longitude': "",
        'altitude': "",
        'start_operation': "",
        'end_operation': "",
        'source': "",
    }

    collection.insert_one(expected)
    return expected


@pytest.fixture
def rs_entry(db):
    collection = db['rainfall_stations']
    mcollection = db['rainfall_measurements']

    expected = {
        "code": str(uuid4()),
        "city": "Baianopolis",
        "state": "Bahia",
        "altitude": 182,
        "geometry": Geometry("FALL", [12, -84])
    }
    measurement = {
        "station_id": expected['code'],
        "date_time": now(),
        "total_rainfall": 32.4,
        "atmospheric_pressure": AtmosphericPressure(23.2, 93.3, 10.4),
        "global_radiation": 32.1,
        "temperature": Temperature(22.2, 23.1, 10.3, 1.0, 3.2, 4.5),
        "humidity": Humidity(23.4, 25.2, 10.4),
        "wind": Wind(38.2, 100.2, 1000.2),
    }
    station = RainfallStation.new(expected)
    measure = RainfallMeasurement.new(measurement)

    collection.insert_one(station.asdict())
    mcollection.insert_one(measure.asdict())
    return station.asdict(), measure.asdict()


def test_route_city(clientinstance, city_entry):
    url = API_PREFIX + '/cities'
    expected = city_entry

    response = clientinstance.get(url)
    assert response.status_code == 200
    assert response.get_json() == expected


def test_route_forecast(clientinstance, db, city_entry):
    url = API_PREFIX + '/forecast?city_id=' + city_entry[0]['_id']
    collection = db['forecast']

    expected = {
        '_id': str(uuid4()),
        'created_at': None,
        'date_time': now(),
        'max_humidity': 100,
        'max_temp': 30,
        'max_temp_trend': '32',
        'min_humidity': 80,
        'min_temp': 26,
        'min_temp_trend': '25',
        'season': 'Fall',
        'source': '',
        'summary': '',
        'sunrise': None,
        'sunset': None,
        'updated_at': None,
        'weather': '',
        'wind_direction': 'west',
        'wind_speed': '12km/h',
        'city_id': city_entry[0]['_id'],
    }

    collection.insert_one(expected)
    expected['date_time'] = expected['date_time'].isoformat()
    del expected['city_id']

    response = clientinstance.get(url)
    assert response.status_code == 200
    assert response.get_json() == [expected]


def test_route_weather_stations(clientinstance, ws_entry):
    url = API_PREFIX + '/weather_stations'
    expected = ws_entry

    response = clientinstance.get(url)
    assert response.status_code == 200
    assert response.get_json() == [expected]


def test_obs_weather(clientinstance, db, ws_entry):
    query = '?station_id=' + ws_entry['_id']
    url = API_PREFIX + '/observed_weather' + query
    collection = db['observed_data']

    expected = {
        '_id': str(uuid4()),
        'station_id': ws_entry['_id'],
        "measurement_date": now(),
        'temp': 37.2,
        'max_temp': None,
        'min_temp': None,
        'avg_temp': None,
        'insolation': None,
        'cloudiness': None,
        'humidity': None,
        'avg_humidity': None,
        'rain': None,
        'wind_speed': None,
        'wind_direction': None,
        'gust': None,
        'created_at': now(),
        'updated_at': now(),
        'pressure': None
    }

    collection.insert_one(expected)
    expected['measurement_date'] = expected['measurement_date'].isoformat()
    expected['created_at'] = expected['created_at'].isoformat()
    expected['updated_at'] = expected['updated_at'].isoformat()

    response = clientinstance.get(url)
    assert response.status_code == 200
    assert response.get_json() == [expected]


def test_obs_check(clientinstance):
    url = API_PREFIX + '/observed_weather/checkpoint'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_rainfall(clientinstance, rs_entry):
    url = API_PREFIX + '/rainfall'
    expected, meas = rs_entry

    response = clientinstance.get(url)
    received = response.get_json()
    del expected['created_at'], expected['updated_at']
    del received[0]['created_at'], received[0]['updated_at']
    assert response.status_code == 200
    assert received == [expected] and meas is not None


def test_rainfall_geo(clientinstance):
    url = API_PREFIX + '/rainfall/geojson'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_rainfall_measure(clientinstance, rs_entry):
    url = API_PREFIX + '/rainfall/' + rs_entry[0]['_id']
    url += '/measurements?day=2022-02-25'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200
