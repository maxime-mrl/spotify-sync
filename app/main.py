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

def get_all_tracks(sp, playlist_id):
  # Retrieve all tracks from a playlist, handling pagination.
  results = sp.playlist_tracks(playlist_id)
  tracks = results['items']
  while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
  return tracks

def cleanup_playlist_directory(directory, expected_files):
  # List audio files (assuming .mp3) and remove those not expected.
  for file in os.listdir(directory):
    file_path = os.path.join(directory, file)
    if os.path.isfile(file_path) and file.lower().endswith('.mp3'):
      base_name = os.path.splitext(file)[0]
      if base_name not in expected_files:
        os.remove(file_path)
        print(f"Removed {file} as it's no longer in the playlist.")

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
if not os.path.exists('downloads'):
  os.mkdir('downloads')
os.chdir('downloads')

# Loop through each playlist and process them
for playlist in playlists['items']:
  playlist_name = playlist['name']
  playlist_url = playlist['external_urls']['spotify']
  print(f"Processing playlist: {playlist_name}")
  
  # Create a safe folder name for the playlist and move to it
  folder_name = normalize_filename(playlist_name)
  folder_name = re.sub(r'\s+', '_', folder_name)
  if not os.path.exists(folder_name):
    os.mkdir(folder_name)
  os.chdir(folder_name)
  
  # Fetch all tracks for this playlist
  tracks = get_all_tracks(sp, playlist['id'])
  
  # Build a set of expected base file names (without extension)
  expected_files = set()
  for item in tracks:
    track = item['track']
    if track is None:  # Skip unavailable tracks
      continue
    # Concatenate all artist names with a comma and space
    artists = ", ".join(artist['name'] for artist in track['artists'])
    expected_base = normalize_filename(f"{artists} - {track['name']}")
    expected_files.add(expected_base)
  
  # Remove files not in the current Spotify playlist
  cleanup_playlist_directory(os.getcwd(), expected_files)
  
  # Run spotdl to download (or update) missing tracks
  command = f'spotdl {playlist_url}'
  subprocess.run(command, shell=True)
  
  # Go back to the downloads folder
  os.chdir('..')

print("All playlists processed!")
