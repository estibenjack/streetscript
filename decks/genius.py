from lyricsgenius import Genius
import os

genius = Genius(os.environ.get('GENIUS_API_KEY'), verbose=False, remove_section_headers=True)

def fetch_lyrics(song_title, artist):
    try:
        song = genius.search_song(song_title, artist)
        if song is None:
            raise Exception("Song not found")
        lyrics = song.lyrics
        return lyrics
    except Exception as e:
        raise Exception(f"Genius API error: {str(e)}")
    
    