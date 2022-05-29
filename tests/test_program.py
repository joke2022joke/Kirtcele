import unittest
from db.database import *
from api.youtube import *


class TestDb(unittest.TestCase):
    def test_create_favorites(self):
        self.assertTrue(CREATE_FAVORITES)

    def test_create_users(self):
        self.assertTrue(CREATE_USERS)

    def test_get_all_user(self):
        self.assertEqual(list, type(get_all_users()))

    def test_adding_users(self):
        self.assertIsNone(add_new_user('User'))

    def test_add_favorite_video(self):
        self.assertIsNone(add_favorite_video('User', 'cat', 'https://www.youtube.com/watch?v=aD-fFyGvDW8',
                         'https://i.ytimg.com/vi_webp/aD-fFyGvDW8/maxresdefault.webp'))

    def test_favorite_video(self):
        self.assertEqual([], select_favorite_videos('Some Video'))


class TestApi(unittest.TestCase):
    def test_videos_popular_get(self):
        self.assertEqual(list, type(videos_popular('UA', 2)))
        with self.assertRaises(KeyError):
            videos_popular(22, 22)
            videos_popular('f', 2)

    def test_videos_by_string_get(self):
        self.assertEqual(list, type(videos_by_string('Cats', 2)))


if __name__ == "__main__":
    unittest.main()
