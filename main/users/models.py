from django.conf import settings
from django.db import models


class WatchlistModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlists"
    )
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ("title", "pk")

    def __str__(self):
        return self.title


class WatchlistItem(models.Model):
    MEDIA_TYPES = (
        ("movie", "Movie"),
        ("tv", "TV show"),
    )

    watchlist = models.ForeignKey(
        WatchlistModel,
        on_delete=models.CASCADE,
        related_name="items"
    )

    tmdb_item_id = models.PositiveIntegerField()

    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ("title", "pk")
        constraints = [
            models.UniqueConstraint(
                fields=("watchlist", "media_type", "tmdb_item_id"),
                name="unique_media_per_watchlist",
            ),
        ]

    def __str__(self):
        return self.title
