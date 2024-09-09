import pytest
from parse_traktor import parse_collection_nml
from io import StringIO
from models import LibraryData

# Sample NML content for testing
SAMPLE_NML = """<?xml version="1.0" encoding="UTF-8"?>
<NML VERSION="19">
    <COLLECTION>
        <ENTRY AUDIO_ID="1" TITLE="Test Track 1" ARTIST="Test Artist 1">
            <LOCATION FILE="file://test/location/track1.mp3" />
            <INFO BITRATE="320" PLAYTIME="300" />
            <TEMPO BPM="128" />
            <ALBUM TITLE="Test Album 1" />
        </ENTRY>
        <ENTRY AUDIO_ID="2" TITLE="Test Track 2" ARTIST="Test Artist 2">
            <LOCATION FILE="file://test/location/track2.mp3" />
            <INFO BITRATE="256" PLAYTIME="240" />
            <TEMPO BPM="125" />
            <ALBUM TITLE="Test Album 2" />
        </ENTRY>
    </COLLECTION>
    <PLAYLISTS>
        <NODE NAME="Test Playlist 1" TYPE="PLAYLIST">
            <ENTRY AUDIO_ID="1" />
        </NODE>
        <NODE NAME="Test Playlist 2" TYPE="PLAYLIST">
            <ENTRY AUDIO_ID="2" />
        </NODE>
    </PLAYLISTS>
</NML>
"""


def test_parse_collection_nml():
    # Use StringIO to simulate a file-like object for the NML content
    nml_file = StringIO(SAMPLE_NML)

    # Call the parsing function
    result = parse_collection_nml(nml_file)

    # Validate the result is a LibraryData object
    assert isinstance(result, LibraryData)

    # Validate tracks
    assert len(result.tracks) == 2

    # Validate the first track
    track1 = result.tracks[0]
    assert track1.track_id == "1"
    assert track1.name == "Test Track 1"
    assert track1.artist == "Test Artist 1"
    assert track1.album == "Test Album 1"
    assert track1.location == "file://test/location/track1.mp3"
    assert track1.bitrate == 320
    assert track1.duration == 300
    assert track1.bpm == 128.0

    # Validate the second track
    track2 = result.tracks[1]
    assert track2.track_id == "2"
    assert track2.name == "Test Track 2"
    assert track2.artist == "Test Artist 2"
    assert track2.album == "Test Album 2"
    assert track2.location == "file://test/location/track2.mp3"
    assert track2.bitrate == 256
    assert track2.duration == 240
    assert track2.bpm == 125.0

    # Validate playlists
    assert len(result.playlists) == 2

    # Validate the first playlist
    playlist1 = result.playlists[0]
    assert playlist1.playlist_name == "Test Playlist 1"
    assert len(playlist1.tracks) == 1
    assert playlist1.tracks[0].track_id == "1"

    # Validate the second playlist
    playlist2 = result.playlists[1]
    assert playlist2.playlist_name == "Test Playlist 2"
    assert len(playlist2.tracks) == 1
    assert playlist2.tracks[0].track_id == "2"

