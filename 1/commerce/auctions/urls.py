from django.urls import path
from . import views
from .views import add_to_watchlist, remove_from_watchlist, show_listing, place_bid, close_auction, add_comment, watchlist, show_categories, show_category_listings
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path('listing/<int:listing_id>/', show_listing, name='show_listing'),
    path('listing/<int:listing_id>/close_auction/', close_auction, name='close_auction'),
    path('listing/<int:listing_id>/add_to_watchlist/', add_to_watchlist, name='add_to_watchlist'),
    path('listing/<int:listing_id>/remove_from_watchlist/', remove_from_watchlist, name='remove_from_watchlist'),
    path('listing/<int:listing_id>/place_bid/', place_bid, name='place_bid'),
    path('listing/<int:listing_id>/add_comment/', add_comment, name='add_comment'),
    path('watchlist/', watchlist, name='watchlist'),
    path('listing/<int:listing_id>/watchlist/', watchlist, name='add_comment'),
    path('categories/', show_categories, name='show_categories'),
    path('categories/<str:category>/', show_category_listings, name='show_category_listings'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)