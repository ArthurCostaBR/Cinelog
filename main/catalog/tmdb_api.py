import requests, os
from dotenv import load_dotenv
from django.utils.translation import get_language

load_dotenv()

class TmdbApi():
    def __init__(self):
        self.api_token = os.getenv("MOVIE_API_TOKEN")
        self.accept = "application/json"
        self.base_url = "https://api.themoviedb.org/3"
        self.language = self._get_language()


        self.headers = {
            "accept": self.accept,
            "Authorization": f"Bearer {self.api_token}"
        }

    def _get_language(self) -> str:
        language = get_language() or "en-US"

        parts = language.split("-")
        if len(parts) == 2:
            language = f"{parts[0].lower()}-{parts[1].upper()}"

        return language

    def search_multi(self, query: str) -> dict:
        params = {
            "language": self.language,
            "page": 1,
            "query": query
        }

        url = f"{self.base_url}/search/multi"

        response = requests.get(url, headers=self.headers, params=params)

        return response.json()

    def popular_movies(self) -> dict:
        params = {
            "language": self.language,
            "page": 1
        }

        url = f"{self.base_url}/movie/popular"

        response = requests.get(url, headers=self.headers, params=params)

        return response.json()

    def popular_tv_shows(self) -> dict:
        params = {
            "language": self.language,
            "page": 1
        }

        url = f"{self.base_url}/tv/popular"

        response = requests.get(url, headers=self.headers, params=params)

        return response.json()