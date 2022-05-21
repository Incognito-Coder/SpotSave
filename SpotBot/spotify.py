import spotdl.search.song_gatherer as Gather
from spotdl.download.downloader import DownloadManager
from spotdl.search import SpotifyClient
import re
import os
import subprocess
from SpotBot.config import Configs

SpotifyClient.init(client_id=Configs.CLIENT_ID,
                   client_secret=Configs.CLIENT_SECRET, user_auth=False)


async def MusicDownloader(query: str = None, format: str = None):
    """
    query: query can be spotify song url or search term
    format: song download format use mp3/m4a/flac/opus/ogg/wav
    """
    global Sname
    global Sartist
    global Filename
    global Scaption
    global IFilename
    global Scover
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if(re.match(regex, query)):
        song = Gather.from_spotify_url(
            spotify_url=query, output_format=format, use_youtube=True)
        Sname = song.song_name
        Sartist = song.album_artists
        Filename = song.file_name+'.' + format
        IFilename = song.file_name+'.mp3'
        Scaption = song.lyrics
        Scover = song.album_cover_url
        with DownloadManager() as DM:
            await DM.download_song(song)
            if format == 'flac':
                print('Converting to flac')
                if os.name == 'nt':
                    subprocess.Popen(['ffmpeg', '-i', song.file_name+'.mp3', Filename],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                else:
                    subprocess.Popen(
                        ["ffmpeg", "-i", song.file_name+'.mp3', Filename, "-map", "1", "-map_metadata", "0", "-c", "copy", "-movflags", "use_metadata_tags"], stdout=subprocess.PIPE).stdout.read()
    else:
        song = Gather.from_search_term(
            query=query, output_format=format, use_youtube=True)
        Sname = song[0].song_name
        Sname = song[0].album_artists
        Filename = song[0].file_name+'.' + format
        IFilename = song[0].file_name+'.mp3'
        Scaption = song[0].lyrics
        Scover = song[0].album_cover_url
        with DownloadManager() as DM:
            await DM.download_song(song[0])
            if format == 'flac':
                print('Converting to flac')
                if os.name == 'nt':
                    subprocess.Popen(['ffmpeg', '-i', song[0].file_name+'.mp3', Filename],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                else:
                    subprocess.Popen(
                        ["ffmpeg", "-i", song[0].file_name+'.mp3', Filename, "-map", "1", "-map_metadata", "0", "-c", "copy", "-movflags", "use_metadata_tags"], stdout=subprocess.PIPE).stdout.read()
Sname = None
Sartist = None
Scaption = None
Filename = None
IFilename = None
Scover = None
