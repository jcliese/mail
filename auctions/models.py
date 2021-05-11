from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    pass


def user_directory_path(instance, filename):
    return 'images/user_{0}/{1}'.format(instance.user.id, filename)

def ending_date():
    return timezone.now() + timedelta(days=14)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    listing_title = models.CharField(max_length=256)
    imgfile = models.ImageField(upload_to = user_directory_path, blank=True)
    min_price = models.FloatField(default=1.0)
    description = models.TextField()
    category = models.CharField(max_length=64)
    time_starting = models.DateTimeField(default=timezone.now)
    time_ending = models.DateTimeField(default=ending_date)

    def __str__(self):
        return self.listing_title    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.FloatField(default=0.0)
    bid_date = models.DateField(default=timezone.now)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")
    comment = models.TextField()
    time_sent = models.DateField(default=timezone.now)

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_items")
    date_added = models.DateTimeField(default=timezone.now)