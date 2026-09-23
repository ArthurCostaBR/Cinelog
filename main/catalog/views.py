from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .tmdb_client import TmdbApi

tmdb = TmdbApi()

@login_required(login_url='/accounts/login/')
def home_view(request):
    context = {
        "movies": tmdb.trending_movies(),
        "shows": tmdb.trending_tv_shows(),
    }
    return render(request, 'home/home.html', context=context)


@login_required(login_url='/accounts/login/')
def search_view(request):
    query = request.GET.get("query", "").strip()

    try:
        page = max(1, int(request.GET.get("page", 1)))
    except (TypeError, ValueError):
        page = 1


    data = {
        "results": [],
        "page": None,
        "total_pages": None,
    }

    if query:
        data = tmdb.search_multi(query=query, page=page)

    context = {
        "results": data["results"],
        "page": data["page"],
        "total_pages": data["total_pages"],
        "query": query
    }
            
    return render(request, 'search/search.html', context=context)


@login_required(login_url='/accounts/login/')
def details_view(request, media_type, tmdb_id):
    context = tmdb.get_details(
        media_type=media_type,
        tmdb_id=tmdb_id,
    )

    context["media_type"] = media_type

    if media_type in ("movie", "tv", "person"):

        template = f"{media_type}/{media_type}.html"

        return render(request, template, context=context)
    

@login_required(login_url='/accounts/login/')
def cast_view(request, media_type, tmdb_id):
    cast = tmdb.get_cast(
        media_type=media_type,
        tmdb_id=tmdb_id,
    )

    context = {
        "cast": cast,
        "media_type": media_type,
        "tmdb_id": tmdb_id,
    }

    if media_type in ("movie", "tv"):
        return render(request, 'cast/cast.html', context=context)