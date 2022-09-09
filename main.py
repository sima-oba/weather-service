import click

from config import Config


@click.group(invoke_without_command=True)
@click.pass_context
def entrypoint(ctx):
    if ctx.invoked_subcommand is None:
        ctx.forward(start_flask_server)


@click.command()
@click.option('--host', default='0.0.0.0', type=click.STRING)  # nosec
@click.option('--port', default=5000, type=click.INT)
def start_flask_server(host: str, port: int):
    from application import rest
    rest.start_flask_server(Config, host, port)


@click.command()
@click.option('--host', default='0.0.0.0', type=click.STRING)  # nosec
@click.option('--port', default=5000, type=click.INT)
@click.option('--workers', default=4, type=click.INT)
def start_gunicorn_server(host: str, port: int, workers: int):
    from application import rest
    rest.start_gunicorn_server(Config, host, port, workers)


@click.command()
def start_kafka_consumer():
    from application import kafka
    kafka.start_consumer(Config)


@click.command()
def init_database():
    from infrastructure import database, repository
    db = database.get_database(Config.MONGODB_SETTINGS)
    repository.init_database(db)


entrypoint.add_command(start_flask_server)
entrypoint.add_command(start_gunicorn_server)
entrypoint.add_command(start_kafka_consumer)
entrypoint.add_command(init_database)


if __name__ == '__main__':
    entrypoint()
