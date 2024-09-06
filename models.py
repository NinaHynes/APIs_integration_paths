from pydantic import BaseModel
from typing import List, Optional, Union  # Added Union for the location field

# Define the Track model
class Track(BaseModel):
    track_id: Optional[str]
    name: Optional[str]
    artist: Optional[str]
    album: Optional[str]
    location: Union[str, dict]  # Allow location to be a string or a dictionary
    bitrate: Optional[int]
    duration: Optional[int]
    bpm: Optional[float]

# Define the Playlist model
class Playlist(BaseModel):
    playlist_name: Optional[str] = None
    tracks: List[Track] = []

# Define the LibraryData model for a uniform response
class LibraryData(BaseModel):
    playlists: List[Playlist] = []
    tracks: List[Track] = []
