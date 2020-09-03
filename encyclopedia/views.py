from django.shortcuts import render, redirect
from markdown2 import markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        content = f"#Whoops! Page not found. Error 404 \n There is no page for **{title}**."

    #convert's the content for markdown
    content = markdown(content)

    return render(request, "encyclopedia/entry.html", {
        'content' : content,
        'title' : title.capitalize()
    })

