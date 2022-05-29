import unittest
import psycopg2.errors
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.pool import SimpleConnectionPool
from env_loading import load_env_variable

DATABASE_URI = load_env_variable("DATABASE_URI")
pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=DATABASE_URI)


class MockDB(unittest.TestCase):
    """
    MockDB class, that was created as database imitation for unit testing.
    """
    @classmethod
    def setUpClass(cls):
        """
        Setting up database for testing. Inside this function
        we define instructions that will run before each test.
        :return: None
        """
        connection = pool.getconn()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        try:
            cursor.execute(f"""DROP DATABASE IF EXISTS Test""")
            print("Database successfully dropped")
        except psycopg2.ProgrammingError as e:
            print(f"Error while dropping database\n{e}")

        try:
            cursor.execute(
                """CREATE DATABASE Test"""
            )
        except psycopg2.OperationalError as e:
            print(f"Failed creating database\n{e}")

        cursor = connection.cursor()

        try:
            cursor.execute("""DROP TABLE IF EXISTS test_table""")
        except psycopg2.OperationalError as e:
            print(f"Failed dropping table\n{e}")

        query = """CREATE TABLE test_table
        (   
            id INTEGER,
            username TEXT PRIMARY KEY 
        )"""

        try:
            cursor.execute(query)
            connection.commit()
        except psycopg2.OperationalError as e:
            print(f"An error has occurred.\n{e}")

    @classmethod
    def tearDownClass(cls):
        """
        This function will run after every test. The tearDown will tide up
        after test method has been run.
        :return: None
        """
        connection = pool.getconn()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        # Drop test database after testing.
        try:
            cursor.execute("""DROP DATABASE Test""")
            connection.commit()

        except psycopg2.OperationalError:
            print("Database Test doesn't exists.")
        connection.close()
