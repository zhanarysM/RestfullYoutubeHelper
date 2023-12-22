from googleapiclient.errors import HttpError
from django.shortcuts import render
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from .utils import get_playlist_length, extract_playlist_id
from .forms import PlaylistForm, TranscribeForm, VideoForm
from .models import Playlist as pl
from .models import Transcript
from pytube import *
from pytube.exceptions import RegexMatchError, AgeRestrictedError


def home(request):
    playlist_length = None
    error_message = None
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_url = form.cleaned_data['playlist_id']
            playlist_id = extract_playlist_id(playlist_url)
            try:
                playlist_length = get_playlist_length(playlist_id)

                if playlist_length is not None:
                    pl.objects.create(playlist_id=playlist_id, playlist_length=playlist_length)
                else:
                    error_message = 'Unable to retrieve playlist length. Please check the playlist ID.'
            except HttpError as e:
                error_message = 'Unable to retrieve playlist length. Please check the playlist ID.'

    else:
        form = PlaylistForm()

    return render(request, 'home.html', {'form': form, 'playlist_length': playlist_length, 'error_message': error_message})

def downloader(request):
    error_message = None
    try:
        if request.method == 'POST':
            link = request.POST['link']
            video = YouTube(link)
            stream = video.streams.get_lowest_resolution()
            stream.download()
    except HttpError as e:
        error_message = "Unable to download. Please check if URL it's correct."
    except RegexMatchError:
        error_message = "Unable to download. Please check if URL it's correct."
    except AgeRestrictedError:
        error_message = 'The video you provided is Age Restricted. Can not download Age Restricted videos.'
    
    return render(request, 'downloader.html', {'error_message':error_message})

def transcriber(request):
    errors_message = None
    video_text = None
    try:
        if request.method == 'POST':
            form = VideoForm(request.POST)
            if form.is_valid():
                video_url = form.cleaned_data['video_url']
                video_id = video_url.split("=")[1].split("&")[0]
                formatter = TextFormatter()
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                video_text = formatter.format_transcript(transcript)
                Transcript.objects.create(video_id=video_id, video_text=video_text)
        else:
            form = TranscribeForm()
    except HttpError as e:
        errors_message = 'Unable to transcribe. Please check if the URL is correct and if the video has captions.' 
    return render(request, 'transcriber.html', {'form':form, 'video_text': video_text, 'errors_message':errors_message})