from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new-page", views.new_page, name="new-page"),
    path("random", views.random_page, name="random"),
    path("<str:entry>", views.entry, name="entry")
]
