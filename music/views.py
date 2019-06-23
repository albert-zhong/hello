from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Album, Song


# Create your views here.
def index(request):
    all_albums = Album.objects.all()
    template = loader.get_template('music/index.html')
    context = {
        'all_albums': all_albums,
    }
    return HttpResponse(template.render(context, request))


def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    context = {
        'album_id': album_id,
        'album': album
    }
    return render(request, 'music/album_index.html', context)


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['fav'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/album_index.html', {
            'album': album,
            'error_message': "you didn't select a favorite song",
        })
    else:
        if selected_song.is_favorite:
            selected_song.is_favorite = False
        else:
            selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'music/album_index.html', {'album': album})
