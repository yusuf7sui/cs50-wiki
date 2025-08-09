from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
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
    result_entries = util.list_entries()
    query = request.GET.get("q", "")        
    result_entries = list(filter(lambda x: query.lower() in x.lower(), result_entries))
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": query}))
    return render(request, "encyclopedia/search-results.html", {
        "results": result_entries
    })
