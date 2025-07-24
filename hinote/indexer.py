import os
from typing import List, Dict
from mutagen import File
from mutagen import MutagenError

SUPPORTED_EXTENSIONS = {'.flac', '.wav', '.alac', '.m4a', '.mp3'}

def scan_music_directory(directory: str) -> List[Dict]:
    songs = []
    song_id = 1
    for root, _, files in os.walk(directory):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                path = os.path.join(root, name)
                metadata = {}
                try:
                    audio = File(path, easy=True)
                    if audio:
                        metadata = audio
                except MutagenError:
                    continue
                song = {
                    'id': song_id,
                    'title': metadata.get('title', [os.path.splitext(name)[0]])[0],
                    'artist': metadata.get('artist', ['Unknown Artist'])[0],
                    'album': metadata.get('album', ['Unknown Album'])[0],
                    'path': path,
                }
                songs.append(song)
                song_id += 1
    return songs
