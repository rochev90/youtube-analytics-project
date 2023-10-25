import os
from googleapiclient.discovery import build
import json
from src.MixinAPI import MixinAPI


class Video(MixinAPI):

    def __init__(self, video_id):
        """Инициализирует video_id"""
        self.__video_id = video_id

        try:
            self.request = Video.get_service().videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=self.__video_id
            ).execute()

            self.title = self.request['items'][0]['snippet']['title']
            self.view_count = self.request['items'][0]['statistics']['viewCount']
            self.like_count = self.request['items'][0]['statistics']['likeCount']
            self.video_url = f"https://www.youtube.com/watch?v={self.__video_id}"

        except IndexError:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.video_url = None
            print("Не верный video_id")


    @property
    def video_id(self):
        """ Делает video_id приватным"""
        return self.__video_id

    def __str__(self):
        """ Возвращает название видео """
        return f"{self.video_title}"

    def print_info(self):
        """ Выводит информацию о видео"""
        print(json.dumps(self.request, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """ Возвращает объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):
    """ Дочерний класс от класса Video"""
    def __init__(self, video_id, playlist_id):
        """Инициализирует id видео и id плейлиста"""
        super().__init__(video_id)
        self.playlist_id = playlist_id

        self.request = PLVideo.get_service().videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id
        ).execute()

        # Берем данные из API
        self.video_title = self.request['items'][0]['snippet']['title']
        self.view_count = self.request['items'][0]['statistics']['viewCount']
        self.like_count = self.request['items'][0]['statistics']['likeCount']
        self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"

