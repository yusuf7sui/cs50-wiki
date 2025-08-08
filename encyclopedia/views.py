from django.shortcuts import render

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
    