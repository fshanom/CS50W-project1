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

def search(request):
    q = request.GET['q']
    if util.get_entry(q):
        #redirect to the existing page calling entry()
        return redirect("entry", title=q)

    #searching for matching entries titles

    #getting all the entries titles in a list
    all_entries = util.list_entries()
    #lowering case of the list and the key to avoid comparision problems
    all_entries = [item.lower() for item in all_entries]
    key = q.lower()
    #making a new list with the matching results
    match_entries = [i for i in all_entries if key in i] 

    #renders the results page passing the list of matching titles
    return render(request, "encyclopedia/search.html",{
        'title' : q,
        'entries' : match_entries
    })