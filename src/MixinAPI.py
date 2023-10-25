import os
from googleapiclient.discovery import build


class MixinAPI:
    api_key: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube