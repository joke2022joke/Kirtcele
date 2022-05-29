# ATTENTION: MAX AMOUNT OF USED QUOTA UNITS PER DAY IS 10000, 1 SEARCH REQUEST COSTS 100 UNITS
# TRY TO MINIMIZE THE AMOUNT OF CALLS TO THE YOUTUBE API!
import requests
from typing import Dict
from env_loading import load_env_variable
from loguru import logger

API_KEY = load_env_variable("API_KEY")


class Video:
    def __init__(self, video_dict=None):
        """
        Represents class necessary video information such as title, url and image url.

        :param video_dict: dict object with parsed video information.
        """
        try:
            self.title = video_dict['snippet']['title']
            self.url = "https://www.youtube.com/watch?v="+video_dict["id"]["videoId"]
            self.img_url = f"http://img.youtube.com/vi/{video_dict['id']['videoId']}/hqdefault.jpg"
            logger.info(f"Successfully created a video from API. Video: {self.title}")
        except TypeError:
            logger.warning("API returned a channel instead of a video.")


def videos_filtration(items: Dict):
    """
    Returns a list of videos by keyword in a form of dict objects.

    :param items: array of dict objects (videos).
    :return: array of dict objects (videos) with 'videoId' key required for gaining urls.
    """
    return [item for item in items if 'videoId' in item['id']]


def videos_by_string(string: str, max_results: int):
    """
    Returns a list of videos by keyword in a form of dict objects.

    :param string: keyword string.
    :param max_results: maximal amount of videos to return (50 = max).
    :return: array of dict objects (videos).
    """
    videos_dict = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={string}&"
                               f"maxResults={max_results}&key={API_KEY}").json()['items']
    logger.info("Performed search by string API request.")
    return [Video(video_dict) for video_dict in videos_filtration(videos_dict)]


def videos_popular(country_code: str, max_results: int):
    """
    Returns a list of most popular videos by country code in a form of dict objects.

    :param country_code: country code, for example ["UA", "RU", "US"].
    :param max_results: maximal amount of videos to return (50 = max).
    :return: array of dict objects (videos).
    """
    videos_dict = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&chart=mostPopular&"
                               f"maxResults={max_results}&key={API_KEY}&regionCode={country_code}").json()['items']
    logger.info("Performed popular videos API request.")
    return [Video(video_dict) for video_dict in videos_filtration(videos_dict)]
