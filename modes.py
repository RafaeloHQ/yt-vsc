from pathlib import Path
import yt_dlp
import os
from yt_dlp import YoutubeDL


def get_opts(mode: str, artist: str) -> dict:

    base = {
        'prefer_ffmpeg': True,
        'quiet': True,
        'noplaylist': True,
        'add_metadata': True,
        'cookiefile': os.path.expanduser("~/Documents/cookies.txt"),
        }

    mode_specifications = {

        'audio': {
            'format': 'bestaudio',
            'outtmpl': str(Path.home() / "Music" / artist / "%(title)s.%(ext)s"),
            'add_metadata': True,
            'prefer_ffmpeg': True,
            'quiet': True,
            'verbose': False,
            'noplaylist': True,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '0',
                },

                {
                    'add_infojson': 'if_exists',
                    'add_metadata': True,
                    'key': 'FFmpegMetadata'
                },

                {'already_have_thumbnail': False,
                'key': 'EmbedThumbnail'},     

                {'key': 'FFmpegMetadata'},  
            ],
            'writethumbnail': True
        },

        'video': {
            'format': 'bestvideo/best',
            'outtmpl': str(Path.home() / "Videos" / artist / "%(title)s.%(ext)s"),
            'merge_output_format': 'mp4',
            'postprocessors': [
                {'key': 'EmbedThumbnail'},

                {
                    'add_infojson': 'if_exists',
                    'add_metadata': True,
                    'key': 'FFmpegMetadata'
                },

                {'key': 'FFmpegMetadata'},  
            ],
        },

        'both': {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': str(Path.home() / "Videos" / artist / "%(title)s.%(ext)s"),
            'prefer_ffmpeg': True,
            'quiet': False,
            'verbose': True,
            'add_metadata': True,
            'noplaylist': True,
            'postprocessors': [

                {'format': 'png',
                'key': 'FFmpegThumbnailsConvertor',
                'when': 'before_dl'},

                {'already_have_thumbnail': False,
                'key': 'EmbedThumbnail'},

                {'key': 'FFmpegMetadata'},

            ],
            'writethumbnail': True
        }
    }
    return {**base, **mode_specifications[mode]}
