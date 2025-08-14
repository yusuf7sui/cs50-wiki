from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import markdown2
import random
random.seed(10)


def index(request):
    """
    Renders the homepage with a list of all encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """
    Renders a specific entry page.
    If the entry doesn't exist, an error page will be shown.
    """
    entry = util.get_entry(title)
    if entry is not None:
        html_content = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html",{
        "title": title,
        "content": html_content
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": entry
        })
    
def search(request):
    """
    If the query matches an existing entry, the user is redirected to that page.
    Otherwise, a search page is rendered, which includes all entries that contain the query as a substring.
    """
    result_entries = util.list_entries()
    query = request.GET.get("q", "")        
    result_entries = list(filter(lambda x: query.lower() in x.lower(), result_entries))
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("entry", kwargs={"title": query}))
    return render(request, "encyclopedia/search-results.html", {
        "results": result_entries
    })

def new_page(request):
    """
    Renders the 'Create New Page' or saves a new entry via POST and redirects to that entry page.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
    return render(request, "encyclopedia/new-page.html")

def random_page(request):
    """
    Redirects to a random entry page.
    """
    result_entries = util.list_entries()
    entries_size = len(result_entries) - 1
    random_entry = result_entries[random.randint(0, entries_size)]
    return HttpResponseRedirect(reverse("entry", kwargs={"title": random_entry}))

def edit_page(request, title):
    """
    Renders the edit page or updates the content of an entry via POST. 
    """
    entry = util.get_entry(title)
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
    return render(request, "encyclopedia/entry-edit.html", {
        "title": title,
        "content": entry
    })

