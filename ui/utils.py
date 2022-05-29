from db import database


def log_in(username):
    database.create_tables()

    # As db cursors always returns tuples, we get the first elements of each)
    usernames_list = [user[0] for user in database.get_all_users()]

    if username not in usernames_list:
        database.add_new_user(username)


def get_favorites_videos(username: str):
    """
    Function used for getting favorites videos for specified name of user.

    :param username: name of the user
    :return: List[Tuple[video_id, user_username, video_name, video_url, video_img_url]]
    """
    return database.select_favorite_videos(username)