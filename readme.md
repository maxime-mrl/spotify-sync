# Spotify playlist sync

This is a simple script that syncs your Spotify playlists with a subsonic capable music hosting platform.

## REQUIREMENTS
for this script to work you MUST meet the following requirements:
- Have a Spotify account + a developer application
- Have a subsonic capable music hosting platform
- Having a nextcloud or owncloud instance handling sync to your music hosting platform
- of course, have python installed and dependencies installed (docker is recommended)

## INSTALLATION
1. Clone this repository
2. create a `.env` file following the structure of `.env~`
3. recommended use with docker

## WARING
1 - This is still in development, it is not really optimized and can be buggy
2 - Technically, this dosen't break spotify TOS since the download is made through youtube.
3 - downloading music you don't own is illegal in most countries. I am not responsible for any illegal use of this script. I made this just for fun and use it with my own music.