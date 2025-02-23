import owncloud
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

oc = owncloud.Client(os.getenv('OWNCLOUD_SERVER'))
oc.login(os.getenv('OWNCLOUD_USER'), os.getenv('OWNCLOUD_PASS'))


def sync_audio():
  remote_folder = os.getenv("MUSIC_FOLDER")
  music_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads', 'songs')
  print("Syncing audio to Nextcloud...")
  # create folder if non existant
  try:
    oc.file_info(remote_folder)
  except owncloud.HTTPResponseError as e:
    # Check for 404 Not Found
    if e.res.status_code == 404:
      oc.mkdir(remote_folder)
    else:
      # Re-raise if it's a different error
      raise

  for audio in os.listdir(music_folder):
    if audio.endswith('.mp3'):
      print(audio)
      oc.put_file(remote_folder + "/" + audio, os.path.join(music_folder, audio))
