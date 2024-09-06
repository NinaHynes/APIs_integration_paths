import pytest
from parse_rekordbox import parse_rekordbox_xml
from io import StringIO

# Sample XML similar to your actual Rekordbox XML
REKORDBOX_XML = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <COLLECTION>
        <TRACK TrackID="1" Name="Test Track 1" Artist="Test Artist 1" Album="Test Album 1"
               Location="file://test/location/track1.mp3" BitRate="320" TotalTime="300" />
        <TRACK TrackID="2" Name="Test Track 2" Artist="Test Artist 2" Album="Test Album 2"
               Location="file://test/location/track2.mp3" BitRate="256" TotalTime="250" />
    </COLLECTION>
    <PLAYLISTS>
        <NODE Name="Test Playlist 1">
            <TRACK Key="1" />
        </NODE>
        <NODE Name="Test Playlist 2">
            <TRACK Key="2" />
        </NODE>
    </PLAYLISTS>
</root>
"""

def test_parse_rekordbox_xml():
    # Use StringIO to simulate a file-like object for the XML content
    xml_file = StringIO(REKORDBOX_XML)

    # Call the parsing function
    result = parse_rekordbox_xml(xml_file)

    # Validate that the correct number of tracks were parsed
    assert len(result.tracks) == 2

    # Validate track 1 data
    track1 = result.tracks[0]
    assert track1.name == "Test Track 1"
    assert track1.artist == "Test Artist 1"
    assert track1.album == "Test Album 1"
    assert track1.location == "file://test/location/track1.mp3"
    assert track1.bitrate == 320
    assert track1.duration == 300

    # Validate track 2 data
    track2 = result.tracks[1]
    assert track2.name == "Test Track 2"
    assert track2.artist == "Test Artist 2"
    assert track2.album == "Test Album 2"
    assert track2.location == "file://test/location/track2.mp3"
    assert track2.bitrate == 256
    assert track2.duration == 250

    # Validate that the correct number of playlists were parsed
    assert len(result.playlists) == 2

    # Validate playlist 1 data
    playlist1 = result.playlists[0]
    assert playlist1.playlist_name == "Test Playlist 1"
    assert len(playlist1.tracks) == 1
    assert playlist1.tracks[0].track_id == "1"

    # Validate playlist 2 data
    playlist2 = result.playlists[1]
    assert playlist2.playlist_name == "Test Playlist 2"
    assert len(playlist2.tracks) == 1
    assert playlist2.tracks[0].track_id == "2"
