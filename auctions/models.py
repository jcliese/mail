from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


def user_directory_path(instance, filename):
    return 'images/user_{0}/{1}'.format(instance.user.id, filename)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    listing_title = models.CharField(max_length=256)
    imgfile = models.ImageField(upload_to = user_directory_path, blank=True)
    min_price = models.FloatField(default=1.0)
    description = models.TextField()
    category = models.CharField(max_length=64)
    pub_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.listing_title

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")
    price = models.FloatField(default=0.0)
    bid_date = models.DateField(default=timezone.now)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")
    comment = models.TextField()
    pub_date = models.DateField(default=timezone.now)