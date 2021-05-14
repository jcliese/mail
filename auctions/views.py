from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist, user_directory_path
from .forms import ImageForm

def index(request):
    listings = Listing.objects.all()
    listings = listings[::-1]
    return render(request, "auctions/index.html", {
        "listings": listings,
        "user_id": request.user.id
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new(request):
    if request.method=="POST":

        username = request.user.username
        user = User.objects.get(username=username)

        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            listing_title = request.POST.get("listing_title")
            if not request.FILES:
                imgfile = None
            else:
                imgfile = request.FILES['imgfile']
            min_price = request.POST.get("min_price")
            description = request.POST.get("description")
            category = request.POST.get("category")
            new_listing = Listing(listing_title=listing_title, imgfile=imgfile, min_price=min_price, description=description, user=user, category=category)
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ImageForm()

    return render(request, "auctions/new.html", {'form' : form})

def listing(request, id):
    try:
        listing = Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        listing = None
    
    on_watchlist = Watchlist.objects.filter(user_id=request.user.id, listing_id=id).exists()
    
    return render(request, "auctions/listing.html", {"listing": listing, "on_watchlist": on_watchlist})

@login_required
def watchlist(request, id):
    if request.method=="POST":
        user = User.objects.get(username=request.user.username)
        listing = Listing.objects.get(id=id)
        on_watchlist = Watchlist.objects.filter(user_id=user, listing_id=id).exists()
        if not on_watchlist:
            entry = Watchlist(user_id=request.user, listing_id=listing)
            entry.save()
        else:
            Watchlist.objects.filter(user_id=user.id, listing_id=listing.id).delete()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
