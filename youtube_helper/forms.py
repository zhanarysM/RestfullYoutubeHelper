from django import forms

class PlaylistForm(forms.Form):
    playlist_id = forms.CharField(label='Enter Playlist ID', max_length=100)
