from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

from env_loading import load_env_variable

DATABASE_URI = load_env_variable("DATABASE_URI")
pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=DATABASE_URI)


@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)

