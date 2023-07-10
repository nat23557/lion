from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db.models import Max
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.contrib import messages



from django.utils import timezone


from .models import User, Listing, Watchlist, Bid, Comment, Watchlist
from .forms import CommentForm, BidForm, CreateListingForm


def index(request):
    # Retrieve all active listings from the database
    active_listings = Listing.objects.filter(active=True)

    return render(request, 'auctions/index.html', {'listings': active_listings})



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            # Check if the user is the winner
            winner_listings = Listing.objects.filter(winner=user)
            for listing in winner_listings:
                messages.success(request, 'Congratulations! You are the winner of the auction for listing: ' + listing.title)

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("index"))


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
def listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return redirect('index')
    else:
        form = CreateListingForm()

    return render(request, 'auctions/listing.html', {'form': form})


def show_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comments = listing.comment_set.all()
    bids = Bid.objects.filter(listing=listing)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.save()
            return redirect('show_listing', listing_id=listing.id)
    else:
        form = CommentForm()

    # Get the current highest bid
    current_price = bids.aggregate(Max('bid_amount')).get('bid_amount__max')

    context = {
        'listing': listing,
        'comments': comments,
        'bids': bids,
        'form': form,
        'current_price': current_price,
    }
    return render(request, 'auctions/show_listing.html', context)

@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listings.add(listing)
    return redirect('show_listing', listing_id=listing_id)

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    watchlist = get_object_or_404(Watchlist, user=request.user)
    watchlist.listings.remove(listing)
    return redirect('show_listing', listing_id=listing_id)



@login_required
def place_bid(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        form = BidForm(request.POST)

        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']

            if bid_amount < listing.starting_bid:
                messages.error(request, 'Bid amount must be greater than the starting bid.')
            else:
                highest_bid = Bid.objects.filter(listing=listing).order_by('-bid_amount').first()
                if highest_bid and bid_amount <= highest_bid.bid_amount:
                    messages.error(request, 'Bid amount must be greater than the current highest bid.')
                else:
                    bid = Bid(listing=listing, bidder=request.user, bid_amount=bid_amount)
                    bid.save()
                    listing.current_price = bid_amount
                    listing.save()

                    messages.success(request, 'Your bid has been placed successfully!')

        else:
            messages.error(request, 'Invalid bid form data.')

        return redirect('show_listing', listing_id=listing.id)

    else:
        return redirect('index')

  
@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # Check if the current user is the creator of the listing
    if request.user == listing.creator:
        # Check if the auction is already closed
        if not listing.active:
            return redirect('show_listing', listing_id=listing_id)

        # Get the highest bid for the listing
        highest_bid = Bid.objects.filter(listing=listing).order_by('-bid_amount').first()


        if highest_bid:
            # Update the listing's active and winner columns
            listing.active = False
            listing.winner = highest_bid.bidder


            # Save the changes to the listing
            listing.save()

            # Announce the winner with a flash message
            messages.success(request, f"The winner of the listing {listing.title} is {listing.winner.username}!")

            return redirect('show_listing', listing_id=listing_id)  # Redirect to the listing page.
    # User is not authorized to close the auction
    return redirect('show_listing', listing_id=listing_id)  # Redirect to the listing page.


@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == 'POST':
        text = request.POST['comment']

        # Create a new comment object and save it to the database
        comment = Comment(listing=listing, user=request.user, text=text)
        comment.save()

        return redirect('show_listing', listing_id=listing.id)

    return render(request, 'auctions/add_comment.html', {'listing': listing})

@login_required
def watchlist(request):
    user = request.user
    watchlist_items = user.watchlist.listings.all()

    for item in watchlist_items:
        bids = Bid.objects.filter(listing=item)
        current_price = bids.aggregate(Max('bid_amount')).get('bid_amount__max')
        item.current_price = current_price if current_price else item.starting_bid

    context = {
        'watchlist_items': watchlist_items,
    }
    return render(request, 'auctions/watchlist.html', context)






def show_categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    context = {
        'categories': categories,
    }
    return render(request, 'auctions/show_categories.html', context)


def show_category_listings(request, category):
    listings = Listing.objects.filter(category=category, active=True)
    context = {
        'category': category,
        'listings': listings,
    }
    return render(request, 'auctions/show_category_listings.html', context)
