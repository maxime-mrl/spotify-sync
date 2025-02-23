import json
import os
import re
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def normalize_filename(s):
  # Remove characters that are not allowed in filenames.
  return re.sub(r'[\\/*?:"<>|]', '', s)

def go_to_folder(name):
  # Create a folder if it doesn't exist and move to it.
  if not os.path.exists(name):
    os.mkdir(name)
  os.chdir(name)

def get_all_tracks(sp, playlist_id):
  # Retrieve all tracks from a playlist, handling pagination.
  results = sp.playlist_tracks(playlist_id)
  tracks = results['items']
  while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
  return tracks

# Initialize Spotipy with OAuth credentials and required scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
  client_id=os.getenv('SPOTIPY_CLIENT_ID'),
  client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
  redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
  scope='playlist-read-private playlist-read-collaborative'
))

# Retrieve current user's playlists
playlists = sp.current_user_playlists()

# Create and move to the output folder
go_to_folder('downloads')

# Loop through each playlist and process them
for playlist in playlists['items']:
  playlist_name = playlist['name']
  playlist_url = playlist['external_urls']['spotify']
  print(f"Processing playlist: {playlist_name}")
  
  # write playlists as JSON
  tracks = get_all_tracks(sp, playlist['id'])

  # Create formatted playlist data
  formatted_data = {
    "name": playlist_name,
    "tracks": [
      {
        "name": track['track']['name'],
        "artist": track['track']['artists'][0]['name'],
        "album": track['track']['album']['name'],
        "release_date": track['track']['album']['release_date'],
        "duration": track['track']['duration_ms'],
        "popularity": track['track']['popularity'],
        "url": track['track']['external_urls']['spotify']
      }
      for track in tracks
    ]
  }
  
  # Write formatted data to JSON
  with open(f'{normalize_filename(playlist_name)}.json', 'w') as f:
    json.dump(formatted_data, f, indent=2)
  
  # # Run spotdl to download (or update) missing tracks
  # go_to_folder('songs')
  # command = f'spotdl {playlist_url}'
  # subprocess.run(command, shell=True)
  # os.chdir('..')
  
print("All playlists processed!")
