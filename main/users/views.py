from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import WatchlistModel, WatchlistItem
from . import services


@login_required(login_url='/accounts/login/')
def profile_view(request):
    if request.method == "POST":
        button = request.POST.get("action")

        if button == "logout":
            logout(request)

            return redirect('accounts:login')

    return render(request, 'profile/profile.html')


@login_required(login_url='/accounts/login/')
def watchlist_view(request):
    watchlists = services.get_user_watchlists(request.user)

    context = {
        "watchlists": watchlists,
    }

    return render(request, "watchlist/watchlist.html", context)


@login_required(login_url='/accounts/login/')
def watchlist_create_view(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()

        if not title:
            messages.error(request, "Enter a name for your watchlist.")
        elif len(title) > 100:
            messages.error(request, "Watchlist names can be up to 100 characters.")
        else:
            watchlist = services.create_watchlist(user=request.user, title=title)
            messages.success(request, "Watchlist created.")
            return redirect("users:watchlist_detail", watchlist_id=watchlist.pk)

    return render(request, "watchlist/create.html", {"title": request.POST.get("title", "")})


@login_required(login_url='/accounts/login/')
def watchlist_detail_view(request, watchlist_id):
    watchlist = get_object_or_404(
        WatchlistModel,
        pk=watchlist_id,
        user=request.user
    )

    items = services.get_watchlist_items(watchlist).select_related("watchlist")

    context = {
        "watchlist": watchlist,
        "items": items,
    }

    return render(request, "watchlist/detail.html", context)


@login_required(login_url='/accounts/login/')
@require_POST
def watchlist_add_item_view(request, watchlist_id):
    watchlist = get_object_or_404(WatchlistModel, pk=watchlist_id, user=request.user)
    raw_id = request.POST.get("tmdb_item_id", "").strip()
    media_type = request.POST.get("media_type", "").strip()
    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()

    try:
        tmdb_item_id = int(raw_id)
    except (TypeError, ValueError):
        tmdb_item_id = 0

    valid_media_types = {choice[0] for choice in WatchlistItem.MEDIA_TYPES}
    if tmdb_item_id < 1 or media_type not in valid_media_types or not title:
        messages.error(request, "Choose a movie or TV show with a valid title.")
    else:
        _, created = services.add_watchlist_item(
            watchlist=watchlist,
            tmdb_item_id=tmdb_item_id,
            media_type=media_type,
            title=title[:255],
            description=description,
        )
        if created:
            messages.success(request, f'"{title}" added to {watchlist.title}.')
        else:
            messages.info(request, f'"{title}" is already in {watchlist.title}.')

    return redirect("users:watchlist_detail", watchlist_id=watchlist.pk)


@login_required(login_url='/accounts/login/')
@require_POST
def watchlist_delete_item_view(request, watchlist_id, item_id):
    watchlist = get_object_or_404(WatchlistModel, pk=watchlist_id, user=request.user)
    deleted = services.delete_watchlist_item(watchlist, item_id)
    if deleted:
        messages.success(request, "Item removed from your watchlist.")
    else:
        messages.error(request, "That item was not found in this watchlist.")
    return redirect("users:watchlist_detail", watchlist_id=watchlist.pk)


@login_required(login_url='/accounts/login/')
@require_POST
def watchlist_update_view(request, watchlist_id):
    watchlist = get_object_or_404(WatchlistModel, pk=watchlist_id, user=request.user)
    action = request.POST.get("action")

    if action == "delete":
        watchlist.delete()
        messages.success(request, "Watchlist deleted.")
        return redirect("users:watchlist")

    if action == "rename":
        title = request.POST.get("title", "").strip()
        if title and len(title) <= 100:
            watchlist.title = title
            watchlist.save(update_fields=("title",))
            messages.success(request, "Watchlist renamed.")
        else:
            messages.error(request, "Enter a name of up to 100 characters.")

    return redirect("users:watchlist_detail", watchlist_id=watchlist.pk)
