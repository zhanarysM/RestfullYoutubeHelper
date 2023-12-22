import os
import re
from datetime import timedelta
from googleapiclient.discovery import build
from django.conf import settings
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


def get_playlists(channel_id):
    api_key = settings.YOUTUBE_API_KEY
    youtube = build('youtube', 'v3', developerKey=api_key)

    playlists = []
    next_page_token = None

    while True:
        request = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=10,
            pageToken=next_page_token,
        )

        response = request.execute()
        playlists.extend(response.get('items', []))
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return playlists

def get_stats(channel_id):
    api_key = settings.YOUTUBE_API_KEY
    youtube = build('youtube', 'v3', developerKey=api_key)

    response = youtube.channels().list(part='statistics', id=channel_id).execute()
    channel_stats = response['items'][0]['statistics']

    context = {
        'channel_stats':channel_stats
    }

    return context

def get_playlist_length(playlist_id):
    api_key = settings.YOUTUBE_API_KEY
    youtube = build('youtube', 'v3', developerKey=api_key)

    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')


    total_seconds = 0

    nextPageToken = None

    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute()

        vid_ids = []
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])

        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(vid_ids)
        )

        vid_response = vid_request.execute()

        for item in vid_response['items']:
            duration = item['contentDetails']['duration']

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_seconds += video_seconds

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            break

    
    total_seconds = int(total_seconds)
    
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    playlist_duration = f'{hours}h:{minutes}m:{seconds}s'

    return playlist_duration

def extract_playlist_id(url):
    pattern = re.compile(r'(?<=list=)[\w-]+')
    match = pattern.search(url)
    return match.group(0) if match else None