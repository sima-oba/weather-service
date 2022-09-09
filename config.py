import logging
import logging.config
import os
import dotenv


dotenv.load_dotenv()


class Config:
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    LOG_DIR = os.getenv('LOG_DIR', './logs')
    INTROSPECTION_URI = os.environ['INTROSPECTION_URI']
    CHECKPOINT = os.getenv('CHECKPOINT', '2015-01-01')
    PROPAGATE_EXCEPTIONS = True
    KAFKA_SERVER = os.environ['KAFKA_SERVER']
    MONGODB_SETTINGS = {
        'db': os.environ['MONGO_DB'],
        'host': os.environ['MONGO_HOST'],
        'port': os.environ['MONGO_PORT'],
        'username': os.environ['MONGO_USER'],
        'password': os.environ['MONGO_PASSWORD'],
        'authentication_source': os.getenv('MONGO_AUTH_SRC', 'admin')
    }


# Set up log
if not os.path.exists(Config.LOG_DIR):
    os.mkdir(Config.LOG_DIR)

if not os.path.isdir(Config.LOG_DIR):
    raise ValueError(f'{Config.LOG_DIR} is not a directory')

logging.config.fileConfig('./logging.ini')
