import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize Spotipy with OAuth credentials and necessary scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='playlist-read-private playlist-read-collaborative'
))

# Retrieve current user's playlists
playlists = sp.current_user_playlists()

print(playlists)

for playlist in playlists['items']:
    print(f"Playlist Name: {playlist['name']}")
    print(f"Description: {playlist.get('description', 'No description')}")
    
    # # Retrieve the tracks for this playlist
    # tracks = sp.playlist_tracks(playlist['id'])
    # print("Songs:")
    # for item in tracks['items']:
    #     track = item['track']
    #     print(f" - {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
    # print("\n" + "-"*40 + "\n")
