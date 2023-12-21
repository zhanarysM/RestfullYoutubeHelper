from django.shortcuts import render, redirect
from .utils import get_stats, get_playlist_length
from .forms import PlaylistForm
from .models import Playlist as pl
from pytube import *
# Create your views here.

# def home(request):
#     channel_id = 'UCI0vQvr9aFn27yR6Ej6n5UA'
#     channel_stats = get_stats(channel_id)

#     return render(request,'home.html', channel_stats)

def home(request):
    playlist_length = None

    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_id = form.cleaned_data['playlist_id']
            # Assuming you have a function to get the playlist length
            playlist_length = get_playlist_length(playlist_id)
            # Save the playlist information in the database
            pl.objects.create(playlist_id=playlist_id, playlist_length=playlist_length)
    else:
        form = PlaylistForm()

    return render(request, 'home.html', {'form': form, 'playlist_length': playlist_length})

def downloader(request):
    if request.method == 'POST':
        link = request.POST['link']
        video = YouTube(link)

        stream = video.streams.get_lowest_resolution()

        stream.download()

        return render(request, 'downloader.html')
    return render(request, 'downloader.html')
