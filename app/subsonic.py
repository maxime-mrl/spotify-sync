import requests
import hashlib
import random
import string
import os
import json
from urllib.parse import urljoin

from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

class SubsonicClient:
  def __init__(self, base_url, username, password):
    self.base_url = base_url
    self.username = username
    self.password = password

  def _make_request(self, endpoint, params={}):
    """Make a request to the Subsonic server"""        
    # Add authentication parameters
    auth_params = {
      'u': self.username,
      'p': self.password,
      'v': '1.16.1',  # API version
      'c': 'sync',   # Client name
      'f': 'json'     # Response format
    }
    
    params.update(auth_params)
    url = urljoin(self.base_url, f'rest/{endpoint}')

    response = requests.get(url, params=params)
    if response.ok != True: return False
    return response.json()

  def ping(self):
    """Test connection to server"""
    response = self._make_request('ping')
    if response == False: return False
    return response['subsonic-response']['status'] == 'ok'

  def get_all_songs(self):
    """Get all songs from the library"""
    songs = self._make_request('search3', {
      "query": "\0",
      "songCount": 9999999,
      "artistCount": 0,
      "albumCount": 0,
      "songOffset": 0,
    })["subsonic-response"]["searchResult3"]["song"]
    return songs
  
  def get_playlist(self, playlist_name):
    """Get playlist ID by name"""
    playlists = self._make_request('getPlaylists')['subsonic-response']['playlists']['playlist']
    for playlist in playlists:
      if playlist['name'] == playlist_name:
        return self._make_request('getPlaylist', {
          'id': playlist['id']
        })["subsonic-response"]["playlist"]
    return self.create_playlist(playlist_name)
  
  def create_playlist(self, playlist_name):
    """Create a new playlist"""
    playlist = self._make_request('createPlaylist', {
      'name': playlist_name
    })['subsonic-response']['playlist']
    return playlist
  
  def update_playlist(self, playlist_id, song_ids):
    """Update a playlist with a list of song IDs"""
    # song_ids = ','.join(song_ids)
    response = self._make_request('updatePlaylist', {
      'playlistId': playlist_id,
      'songIdToAdd': song_ids
    })
    return response['subsonic-response']['status'] == 'ok'
  
  def scan_library(self):
    """Scan the library for new files and wait until scanning is complete"""
    
    # Start scan if not already scanning
    status = self._make_request('getScanStatus')['subsonic-response']['scanStatus']
    if not status['scanning']:
      print("Starting scan...")
      print(self._make_request('scan')['subsonic-response'])

    elapsed = 0
    # Wait until scan is complete
    while elapsed < 60: # max 60 seconds of scanning time
      elapsed += 1
      status = self._make_request('getScanStatus')['subsonic-response']['scanStatus']
      if not status['scanning']:
        return True
      time.sleep(1)  # Wait 1 second before checking again
    
    return False

# testing da shit
if __name__ == "__main__":
    
    # Replace these with your actual Subsonic server details
    SERVER_URL = os.getenv('SUBSONIC_SERVER')
    USERNAME = os.getenv('SUBSONIC_USER')
    PASSWORD = os.getenv('SUBSONIC_PASS')

    # Create client instance
    client = SubsonicClient(os.getenv('SUBSONIC_SERVER'), os.getenv('SUBSONIC_USER'), os.getenv('SUBSONIC_PASS'))

    # Test connection
    if client.ping():
        print("Successfully connected to Subsonic server")
        print("iniate scan")
        print(client.scan_library())
        # Get all songs
        songs = client.get_all_songs()
        
        # Update playlist with song in json file
        # with open("./downloads/test-playlist.json", "r") as f:
        #   d = json.load(f)
        #   to_add = []
        #   for track in d["tracks"]:
        #     for song in songs:
        #       if song['title'] == track:
        #         to_add.append(song["id"])
        #   playlist_id = client.get_playlist_id(d["name"])
        #   print(client.update_playlist(playlist_id, to_add))
    else:
        print("Failed to connect to Subsonic server")