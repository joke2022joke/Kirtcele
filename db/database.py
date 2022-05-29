from contextlib import contextmanager
from db.connection_pool import get_connection

# region ---------------DATABASE QUERIES------------------
CREATE_USERS = """
    CREATE TABLE IF NOT EXISTS users
    (
        username TEXT PRIMARY KEY
    );
"""

CREATE_FAVORITES = """
    CREATE TABLE IF NOT EXISTS favorites
    (
        id SERIAL,
        user_username TEXT,
        video_name TEXT,
        video_url TEXT,
        video_img_url TEXT,
        PRIMARY KEY(user_username, video_url),
        FOREIGN KEY(user_username) REFERENCES users(username)
    );    
"""

INSERT_USER = """INSERT INTO users VALUES (%s);"""
INSERT_FAVORITE = """INSERT INTO favorites (user_username, video_name, video_url, video_img_url) 
                     VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;"""

SELECT_USERS = """SELECT * FROM users;"""
SELECT_FAVORITES = """SELECT * FROM favorites WHERE user_username=%s;"""
DELETE_FAVORITE = """DELETE FROM favorites WHERE video_name=%s AND user_username=%s;"""
# endregion


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables():
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(CREATE_USERS)
            cursor.execute(CREATE_FAVORITES)


def get_all_users():
    """
    Allows to get info about all users.

    :return: List[Tuple[str: user name]]
    """
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(SELECT_USERS)
            return cursor.fetchall()


def add_new_user(user_username: str):
    """
    Add new user to the user database table.

    :param user_username: name of the user
    :return: None
    """
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(INSERT_USER, (user_username,))


def add_favorite_video(user_username: str,
                       video_name: str,
                       video_url: str,
                       video_img_url: str):

    """
    Add video to 'favorites' for specified user.

    :param user_username: name of the user
    :param video_name: name of the video
    :param video_url: url of the video
    :param video_img_url: url of the video preview image
    :return: None
    """
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(INSERT_FAVORITE, (user_username, video_name, video_url, video_img_url))


def select_favorite_videos(user_username: str):
    """
    Allows to get the information about all favorite videos for specified user.

    :param user_username: name of the user
    :return: List[Tuple[info row for each favorite video]]
    """
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(SELECT_FAVORITES, (user_username,))
            return cursor.fetchall()


def delete_favorite_video(movie_name: str, user_username: str):
    """
    Delete favorite video from list for specified user.

    :param movie_name: name of the movie
    :param user_username: name of the user
    :return: None
    """
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(DELETE_FAVORITE, (movie_name, user_username))
