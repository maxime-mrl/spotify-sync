import json
import os
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from utils import normalize_filename, go_to_folder

# Load environment variables from .env file
load_dotenv()

def download_songs():
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
        track['track']['name'] for track in tracks
      ]
    }
    # Write formatted data to JSON
    with open(f'{normalize_filename(playlist_name)}.json', 'w') as f:
      json.dump(formatted_data, f, indent=2)
    
    # Run spotdl to download missing tracks
    go_to_folder('songs')
    command = f'spotdl {playlist_url}'
    subprocess.run(command, shell=True)
    os.chdir('..')
  print("All playlists processed!")


def get_all_tracks(sp, playlist_id):
  # Retrieve all tracks from a playlist, handling pagination.
  results = sp.playlist_tracks(playlist_id)
  tracks = results['items']
  while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
  return tracks
