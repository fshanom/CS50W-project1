from django.shortcuts import render, redirect
from django import forms
from markdown2 import markdown
import random
from django.contrib import messages

from . import util

class PageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Content",  widget=forms.Textarea(attrs={'class': 'form-control'}))

class EditForm(PageForm):
    title = None

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        content = f"#Whoops! Page not found. Error 404 \n There is no page for **{title}**."

    #convert's the content for html
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

    #ignoring case sensitivity to avoid comparision problems
    match_entries = [i for i in all_entries if q.casefold() in i.casefold()] 

    #renders the results page passing the list of matching titles
    return render(request, "encyclopedia/search.html",{
        'title' : q,
        'entries' : match_entries
    })

#show a form to the user and create a new page
def create(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page_title = form.cleaned_data["title"]
            page_content = form.cleaned_data["content"]
            if util.get_entry(page_title) == None:
                util.save_entry(page_title, page_content)
                return redirect("entry", title=page_title)
            else:
                messages.error(request,'ERROR. A page with this title already exists')
                return render(request, "encyclopedia/create.html", {
                'form' : form
                })
        else:
            return render(request, "encyclopedia/create.html", {
                'form' : form
            })
    else:    
        return render(request, "encyclopedia/create.html", {
            'form' : PageForm()
        })

#load the existing text in the page to changes and writes it to the file
def edit(request, title):
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        form = EditForm(initial={"content":util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            'title' : title,
            'form' : form
        })    

#load a random page
def random_page(request):
    title_list = util.list_entries()
    random_title = random.choice(title_list)
    return redirect("entry", title=random_title)