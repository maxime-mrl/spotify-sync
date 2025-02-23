import os
import re
import subprocess
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

# output folder
if not os.path.exists('downloads'):
  os.mkdir('downloads')
os.chdir('downloads')

# Loop through each playlist and download them
for playlist in playlists['items']:
    playlist_name = playlist['name']
    playlist_url = playlist['external_urls']['spotify']
    print(f"Downloading playlist: {playlist_name}")
    # create folder for each playlists
    playlist_name = re.sub(r'[\\/*?:"<>|]', '', playlist_name)
    playlist_name = re.sub(r'\s+', '_', playlist_name)
    if not os.path.exists(playlist_name):
      os.mkdir(playlist_name)
    os.chdir(playlist_name)
    
    # Run spotdl to download the playlist
    command = f'spotdl {playlist_url}'
    subprocess.run(command, shell=True)
    # go back to downloads folder
    os.chdir('..')

print("All playlists downloaded!")
