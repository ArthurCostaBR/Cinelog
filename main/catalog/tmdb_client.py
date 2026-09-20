import requests, os
from dotenv import load_dotenv
from django.utils.translation import get_language

load_dotenv()

class TmdbApi():
    """Client for retrieving and formatting data from the TMDB API."""

    def __init__(self):
        """Initialize the TMDB client with authentication and API settings."""

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
        """Search TMDB for movies, TV shows, and people and return relevant results."""

        params = {
            "language": self._get_language(),
            "page": page,
            "query": query
        }

        url = f"{self.base_url}/search/multi"

        response = requests.get(url=url, headers=self.headers, params=params)
        response.raise_for_status()
        response = response.json()

        results = []

        for result in response["results"]:
            if not (result.get("poster_path") or result.get("profile_path")):
                continue

            if result.get("popularity", 0) < 0.4:
                continue

            if result.get("vote_count", 0) <= 1:
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


    def trending_movies(self, time_window: str="day") -> list[dict]:
        """Return up to nine trending movies for the given time window."""

        params = {
            "language": self._get_language(),
            "page": 1,
        }

        url = f"{self.base_url}/trending/movie/{time_window}"

        response = requests.get(url=url, headers=self.headers, params=params)
        response.raise_for_status()
        response = response.json()

        movie_list = []

        for result in response["results"]:
            if len(movie_list) < 9:
                movie_list.append({
                    "id": result.get("id"),
                    "title": result.get("title"),
                    "poster": result.get("poster_path"),
                    "release_date": result.get("release_date"),
                })

        return movie_list


    def trending_tv_shows(self, time_window: str="day") -> list[dict]:
        """Return up to nine trending TV shows for the given time window."""

        params = {
            "language": self._get_language(),
            "page": 1,
        }

        url = f"{self.base_url}/trending/tv/{time_window}"

        response = requests.get(url=url, headers=self.headers, params=params)
        response.raise_for_status()
        response = response.json()

        shows_list = []

        for result in response["results"]:
            if len(shows_list) < 9:
                shows_list.append({
                    "id": result.get("id"),
                    "title": result.get("name"),
                    "poster": result.get("poster_path"),
                    "release_date": result.get("first_air_date"),
                })

        return shows_list


    def get_details(self, media_type: str, tmdb_id: int) -> dict:
        """Return all data required to render a movie, TV show, or person detail page."""

        details = self._fetch_details(media_type, tmdb_id)
        credits = self._fetch_credits(media_type, tmdb_id)

        top_billed_cast = []
        main_jobs = []
        person_credits = []

        if media_type in ("movie", "tv"):
            top_billed_cast = self._top_billed_cast(credits.get("cast", []))
            main_jobs = self._main_jobs(credits.get("crew", []))

        elif media_type == "person":
            person_credits = self._person_credits(credits=credits)

        return {
            "details": details,
            "credits": credits,
            "top_billed_cast": top_billed_cast,
            "main_jobs": main_jobs,
            "person_credits": person_credits,
        }

        
    def _fetch_details(self, media_type: str, tmdb_id: int) -> dict:
        """Fetch detailed information for a movie, TV show, or person from TMDB."""

        params = {
            "language": self._get_language(),
        }

        url = f"{self.base_url}/{media_type}/{tmdb_id}"

        response = requests.get(url=url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()
    

    def _fetch_credits(self, media_type: str, tmdb_id: int) -> dict:
        """Fetch credits for a movie, TV show, or person from TMDB."""

        params = {
            "language": self._get_language(),
        }

        url = f"{self.base_url}/{media_type}/{tmdb_id}"

        if media_type == "tv":
            url = f"{url}/aggregate_credits"

        elif media_type == "person":
            url = f"{url}/combined_credits"

        else:
            url = f"{url}/credits"

        response = requests.get(url=url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()


    def _person_credits(self, credits: dict) -> dict[str, list[dict]]:
        """Group a person's relevant cast and crew credits by department."""

        response = {
            "Acting": []
        }

        unwanted_characters = [
            "Self - Host", 
            "Self", 
            "Self - Guest",
            "Self - Presenter"
            ]

        for result in credits.get("cast", []):
            if result.get("popularity", 0) < 0.4:
                continue

            release_date = result.get("release_date") or result.get("first_air_date")

            if not release_date:
                continue

            if result.get("character") in unwanted_characters:
                continue

            if result.get("vote_count", 0) <= 1:
                continue

            response["Acting"].append({
                "id": result.get("id"),
                "title": result.get("title") or result.get("name"),
                "release_date": result.get("release_date") or result.get("first_air_date"),
                "job": result.get("character"),
                "media_type": result.get("media_type")
            })

        for result in credits.get("crew", []):
            if result.get("popularity", 0) < 0.4:
                continue

            release_date = result.get("release_date") or result.get("first_air_date")

            if not release_date:
                continue

            department = result.get("department") or "Crew"

            if department not in response:
                response[department] = []

            response[department].append({
                "id": result.get("id"),
                "title": result.get("title") or result.get("name"),
                "release_date": result.get("release_date") or result.get("first_air_date"),
                "job": result.get("job"),
                "media_type": result.get("media_type")
            })

        for department_credits in response.values():
            department_credits.sort(
                key=lambda credit: credit.get("release_date") or "",
                reverse=True
            )

        return response


    def _top_billed_cast(self, cast: list[dict]) -> list[dict]:
        """Return up to nine cast members with available profile images."""

        response = []

        for person in cast:
            if len(response) >= 9:
                break

            if person.get("profile_path"):
                response.append({
                    "id": person.get("id"),
                    "name": person.get("name"),
                    "character": person.get("character"),
                    "profile_path": person.get("profile_path"),
                })

        return response


    def _main_jobs(self, crew: list[dict]) -> list[dict]:
        """Return crew members credited in selected primary creative roles."""

        relevant_jobs = (
            "Director", 
            "Screenplay", 
            "Novel", 
            "Writer", 
            "Story", 
            "Teleplay"
            )
        
        response = []
    
        for person in crew:
            job = person.get("job")

            if job in relevant_jobs:
                response.append({
                    "id": person.get("id"),
                    "name": person.get("name"),
                    "job": job,
                })

        return response