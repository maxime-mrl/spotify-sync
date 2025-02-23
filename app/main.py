import os
import json

from download import download_songs
from subsonic import SubsonicClient
from nextcloud import sync_audio


def main():
  # 1- Download songs from Spotify
  download_songs()
  # 2- Sync downloaded songs to Nextcloud
  sync_audio() # can throw too many requests error sometimes
  # 3- Sync downloaded songs to Subsonic
  subsonic = SubsonicClient(
    os.getenv('SUBSONIC_SERVER'),
    os.getenv('SUBSONIC_USER'),
    os.getenv('SUBSONIC_PASS')
  )
  # Test connection to server
  if subsonic.ping() == False:
    print("Could not connect to Subsonic server")
    return
  # initiate subsonic scan
  subsonic.scan_library()
  # get all songs
  songs = subsonic.get_all_songs()
  # sync the playlist
  json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
  for file in os.listdir(json_path):
    if file.endswith('.json'):
      with open(os.path.join(json_path, file), "r") as f:
        list = json.load(f)
        to_add = []
        for track in list["tracks"]:
          for song in songs:
            if song['title'] == track:
              to_add.append(song["id"])
        playlist_id = subsonic.get_playlist_id(list["name"])
        print(subsonic.update_playlist(playlist_id, to_add))

main()
  