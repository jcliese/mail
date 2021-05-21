from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import User, Listing, Bid, Watchlist, Comment
from .forms import ImageForm, BidForm, CommentForm, all_categories

def check_active(request):
    request.session['watchlist_length'] = len(Watchlist.objects.filter(user_id=request.user))
    listings = Listing.objects.all()
    for listing in listings:
        if listing.time_ending < timezone.now():
            listing.is_active = False
            listing.save()

def get_current_price(listings):
    for listing in listings:
        bids = Bid.objects.filter(listing_id=listing.id).values_list('price', flat=True).order_by('-id')
        if bids:
            current_price = bids[0]
        else:
            current_price = listing.min_price

        listing.current_price = current_price
    return listings

def index(request):
    print(request.session['watchlist_length'])
    check_active(request)
    listings = Listing.objects.filter(is_active=True)
    listings = listings[::-1]
    listings = get_current_price(listings)
    print("INDEX", listings)

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
    check_active(request)
    try:
        listing = Listing.objects.get(id=id)
    except Listing.DoesNotExist:
        listing = None
    
    on_watchlist = Watchlist.objects.filter(user_id=request.user.id, listing_id=id).exists()

    bids = Bid.objects.filter(listing_id=listing.id).order_by('-id')
    comments = Comment.objects.filter(listing_id=listing.id).order_by('-id')
    if bids:
        current_price = bids.values_list('price', flat=True)[0]
        highest_bidder = bids.values_list('user_id', flat=True)[0]
    else:
        current_price = listing.min_price
        highest_bidder = None
    listing.current_price = current_price
    listing.highest_bidder = highest_bidder
    
    bid_form = BidForm(listing.min_price)
    comment_form = CommentForm()
    return render(request, "auctions/listing.html", {"listing": listing, "on_watchlist": on_watchlist, "bid_form": bid_form, "user": request.user, "numb_bids": len(bids), "comments": comments, "comment_form": comment_form })

def category(request, cat):
    check_active(request)
    listings = Listing.objects.filter(category=cat, is_active=True)
    listings = listings[::-1]
    listings = get_current_price(listings)
    category = next(item for item in all_categories() if item["category"] == cat)
    return render(request, "auctions/category.html", {"listings": listings, "category": category})

@login_required
def watchlist(request):
    check_active(request)
    watchlist_items = Watchlist.objects.filter(user_id=request.user)
    listings = []
    for item in watchlist_items:
        listing = Listing.objects.get(id=item.listing_id.id)
        listings.append(listing)
    listings = listings[::-1]
    listings = get_current_price(listings)

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def change_watchlist(request, id):
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

@login_required
def bid(request, id):
    if request.method=="POST":
        user = User.objects.get(username=request.user.username)
        listing = Listing.objects.get(id=id)
        all_bids = Bid.objects.filter(listing_id=id)
        bid_price = request.POST.get("bid_price")
        new_bid = Bid(user_id=request.user, listing_id=listing, price=bid_price)
        new_bid.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def close(request, id):
    if request.method=="POST":
        listing = Listing.objects.get(id=id)
        listing.is_active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

@login_required
def comment(request, id):
    if request.method=="POST":
        listing = Listing.objects.get(id=id)
        comment = request.POST.get("comment")
        new_comment = Comment(user=request.user, listing=listing, comment=comment)
        new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
