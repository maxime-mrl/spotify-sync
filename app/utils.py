import os
import re


def normalize_filename(s):
  # Remove characters that are not allowed in filenames.
  return re.sub(r'[\\/*?:"<>|]', '', s)

def go_to_folder(name):
  # Create a folder if it doesn't exist and move to it.
  if not os.path.exists(name):
    os.mkdir(name)
  os.chdir(name)