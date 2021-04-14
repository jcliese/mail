from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    category = models.CharField(max_length=64)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Bids")
    price = models.FloatField()
    bid_date = models.DateField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Comments")
    comment = models.CharField(max_length=2048)