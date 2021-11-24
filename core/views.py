from django.shortcuts import render, redirect
from .utils import SearchAnime, isAvailable, isUnavailable, NotFound, CheckAvailability
from .utils import getAnimeName

def welcome_view(request):
    template_name = "core/index.html"
    return render(request, template_name)


def RedirectView(request):
    return redirect("https://google.com/")


def APIScanner(request):
    if request.method == 'POST':
        anime_name = request.POST.get('animeName')
        content = SearchAnime(anime_name)
        
        if CheckAvailability(content.text)=='available':
            context = {
                'anime':getAnimeName(content.text),
                'status':'available',
                "watch_link":content.url,
            }
            print(context)
            return render(request, 'core/outcome.html', context)

        elif CheckAvailability(content.text)=='unavailable':
            context = {
                'anime':getAnimeName(content.text),
                'status':'unavailable',
            }
            print(context)
            return render(request, 'core/outcome.html', context)

        else:
            context = {
                'anime':anime_name,
                'status':"NA",
            }
            print(context)
            return render(request, 'core/outcome.html', context)
        