from django import forms

class PlaylistForm(forms.Form):
    playlist_id = forms.CharField(label='Enter Playlist ID', max_length=100)

class TranscribeForm(forms.Form):
    video_id = forms.CharField(label='Enter Video Link', max_length=100)    

class VideoForm(forms.Form):
    video_url = forms.URLField()