from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import markdown2


def index(request):
    """
    Renders the homepage with a list of all encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    """
    Renders a specific entry page.
    If the entry doesn't exist, an error page will be shown.
    """
    entry = util.get_entry(entry)
    if entry is not None:
        html_content = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html",{
        "title": entry,
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
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": query}))
    return render(request, "encyclopedia/search-results.html", {
        "results": result_entries
    })

def new_page(request):
    """
    If the create click button is clicked the create new page is rendered.
    When the form is submitted via POST with a title and content,
    the entry will be saved and the user is redirected to the new entry page.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
    return render(request, "encyclopedia/new-page.html")
    
