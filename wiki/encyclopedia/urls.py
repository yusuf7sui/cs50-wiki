from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new-page", views.new_page, name="new-page"),
    path("random", views.random_page, name="random"),
    path("<str:title>", views.entry, name="entry"),
    path("<str:title>/edit", views.edit_page, name="edit")
]
