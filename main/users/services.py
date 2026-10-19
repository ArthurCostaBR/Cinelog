from .models import WatchlistModel, WatchlistItem


def get_user_watchlists(user):
    return WatchlistModel.objects.filter(user=user).prefetch_related("items")


def create_watchlist(user, title):
    return WatchlistModel.objects.create(
        user=user,
        title=title
    )


def get_watchlist_items(watchlist):
    return watchlist.items.all()


def add_watchlist_item(watchlist, tmdb_item_id, media_type, title, description=""):
    return WatchlistItem.objects.get_or_create(
        watchlist=watchlist,
        tmdb_item_id=tmdb_item_id,
        media_type=media_type,
        defaults={"title": title, "description": description},
    )


def delete_watchlist_item(watchlist, item_id):
    return watchlist.items.filter(pk=item_id).delete()[0] > 0
