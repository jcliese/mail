from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
    path("listing/<int:id>/close", views.close, name="close")
] 
