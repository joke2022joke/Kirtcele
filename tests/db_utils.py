import psycopg2.errors
from psycopg2.pool import SimpleConnectionPool
from env_loading import load_env_variable

DATABASE_URI = load_env_variable("DATABASE_URI")
pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=DATABASE_URI)

connection = pool.getconn()
cursor = connection.cursor()


def db_read(query):
    """
    Function, that was created to read data from database for every test.
    :param query: commands, to retrieve data from database.
    :return: True or False
    """
    try:
        cursor.execute(query)

        entries = cursor.fetchall()
        cursor.close()
        connection.close()

        content = []

        for entry in entries:
            content.append(entry)
        return content

    except psycopg2.InterfaceError as e:
        print("An error hac occurred.\n", e)
        return False


def db_write(query):
    """
    Function that was created to write data to database for every test.
    :param query: commands, to write data to database.
    :return: True or False
    """
    try:
        cursor.execute(query)
        connection.commit()
        return True

    except psycopg2.ProgrammingError as e:
        print("An error has occurred.\n", e)
        return False
