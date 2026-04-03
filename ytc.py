from yt_dlp import YoutubeDL
import sys
import re
from pathlib import Path
from yt_dlp.utils import DownloadError
from modes import get_opts
import os


 

#checks if the link is a Youtube link using regex, returns bool
def input_check(link: str) -> bool:
    
    #regex filter
    youtube = re.compile(r"^(https?://)?(www\.)?(music\.youtube\.com|youtube\.com|youtu\.be)/.+$")
    reddit = re.compile(r"^(https?://)?(www\.)?(reddit\.com)/.+$")
    #checks if variable link matches the regex filter
    if youtube.match(link):
        print( "[Youtube] Valid Link! " + link )
        return True
    elif reddit.match(link):
         print( "[Reddit] Valid Link! " + link )
         return True
    else:
        print( "[Website] Invalid Link! " + link)
        return False
        exit(1) #terminates the whole program, raises error code 1
    
def artist_sanitization(info: dict) -> dict:
    
    if info.get("_type") == "playlist":
        for entry in info['entries']:
            artist = entry.get("artist") or entry.get("uploader") or "Unspecified"
            entry['artist'] = artist.split(",")[0].strip()
    else:
        artist = info.get("artist") or info.get("uploader") or "Unspecified"
        info['artist'] = artist.split(",")[0].strip()
    
    return info

def download(link: str, isWhat: str = "audio", isAlbum: bool = False):

    
    ##checks what mode to download on
    if isWhat not in {"audio", "video", "both"}:
        raise ValueError(f"[YT-DLP] Invalid mode: {isWhat}")

    ##announces download starting
    print(f"[YT-DLP] Starting {isWhat} download for {link}")

    try: #preliminary metadata request
        with YoutubeDL({'quiet': True, 'skip_download': True, 'noplaylist': False, 'cookiefile': os.path.expanduser("~/Documents/cookies.txt")}) as ydl:
            info = ydl.extract_info(link, download=False)
            if info.get('_type') != 'playlist':
                #clears the artist field inside the info dictionary
                print("#####UNPROCESSED#####")
                print(info.get('artist'))
                info = artist_sanitization(info)
                print("#####PROCESSED#####")
                print(info.get('artist'))
            info = artist_sanitization(info)

        #obtains the artist field from the info dictionary
        artist = info.get('artist') if info.get('_type') != 'playlist' else info['entries'][0]['artist']
        #get the appropriate opts based on isWhat, fix the artist and store it in variable opts
        opts = get_opts(isWhat, artist)
        
        if isAlbum and info.get("_type") == "playlist":
            
            #find the right category path based on isWhat
            #store it to a variable localldir
            localdir={
                'audio': "Music",
                'video': "Videos",
                'both': "Videos"
            }.get(isWhat)
            
            playlist_name=info['title']
            playlist_name=playlist_name.replace("Album -", "").replace("Album", "").strip()
            opts['noplaylist'] = False
            opts['outtmpl'] = str(Path.home() / localdir / artist / playlist_name / "%(title)s.%(ext)s")

        with YoutubeDL(opts) as ydl:
            if info.get('_type') == 'playlist':
                print(f"[YT-DLP] Downloading Playlist: {link}")
                for entry in info['entries']:
                    ydl.process_info(entry)
            else:
                ydl.process_info(info)
                    
    except DownloadError as e:
        if "cookies" in str(e).lower():
            print(f"[YT-DLP] Cookie Error Detected. Please rotate cookie.txt")
            sys.exit(1)




   
           