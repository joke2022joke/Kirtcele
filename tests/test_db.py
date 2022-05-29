import db_utils
from mock_database import MockDB
from unittest.mock import patch


class TestDB(MockDB):
    @patch('mock_database.MockDB')
    def test_01_db_write(self, *params):
        self.assertEqual(db_utils.db_write("""INSERT INTO test_table(id, username) VALUES(1, 'Van')"""), True)

    @patch('mock_database.MockDB')
    def test_02_db_read(self, *params):
        self.assertEqual(db_utils.db_write("""SELECT * FROM test_table"""), True)