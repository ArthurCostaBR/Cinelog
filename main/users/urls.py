from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("watchlist/", views.watchlist_view, name="watchlist"),
    path("watchlist/create/", views.watchlist_create_view, name="watchlist_create"),
    path("watchlist/<int:watchlist_id>/", views.watchlist_detail_view, name="watchlist_detail"),
    path("watchlist/<int:watchlist_id>/update/", views.watchlist_update_view, name="watchlist_update"),
    path("watchlist/<int:watchlist_id>/items/add/", views.watchlist_add_item_view, name="watchlist_add_item"),
    path(
        "watchlist/<int:watchlist_id>/items/<int:item_id>/delete/",
        views.watchlist_delete_item_view,
        name="watchlist_delete_item",
    ),
]
