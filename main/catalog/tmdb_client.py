import requests, os
from dotenv import load_dotenv
from django.utils.translation import get_language

load_dotenv()

class TmdbApi():
    def __init__(self):
        self.api_token = os.getenv("MOVIE_API_TOKEN")
        self.accept = "application/json"
        self.base_url = "https://api.themoviedb.org/3"

        self.headers = {
            "accept": self.accept,
            "Authorization": f"Bearer {self.api_token}"
        }


    def _get_language(self) -> str:
        """Return the browser language normalized with TMDB format (xx-YY)."""

        language = get_language() or "en-US"

        parts = language.split("-")
        if len(parts) == 2:
            language = f"{parts[0].lower()}-{parts[1].upper()}"

        return language


    def search_multi(self, query: str, page: int) -> dict:
        """Filter out irrelevant results and return TMDB search results for movies, TV shows, and people."""

        params = {
            "language": self._get_language(),
            "page": page,
            "query": query
        }

        url = f"{self.base_url}/search/multi"

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        response = response.json()

        results = []

        for result in response["results"]:
            if not (result.get("poster_path") or result.get("profile_path")):
                continue

            if result.get("popularity", 0) < 0.3:
                continue

            known_for = []
                            
            for movie in result.get("known_for", []):
                known_for.append({"title": movie.get("title") or movie.get("name")})

            results.append({
                "id": result.get("id"),
                "name": result.get("name") or result.get("title"),
                "media_type": result.get("media_type"),
                "release_date": result.get("release_date") or result.get("first_air_date"),
                "score": result.get("vote_average"),
                "poster": result.get("poster_path") or result.get("profile_path"),
                "overview": result.get("overview"),
                "known_for": known_for
            })

        return {
            "results": results,
            "page": response.get("page"),
            "total_pages": response.get("total_pages")
        }


    def popular_movies(self) -> dict:
        """Return a dict with the most popular movies on TMDB."""

        params = {
            "language": self._get_language(),
            "page": 1
        }

        url = f"{self.base_url}/movie/popular"

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()


    def popular_tv_shows(self) -> dict:
        """Return a dict with the most popular TV shows on TMDB."""

        params = {
            "language": self._get_language(),
            "page": 1
        }

        url = f"{self.base_url}/tv/popular"

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()