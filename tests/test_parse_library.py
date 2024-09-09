import pytest
from parse_apple_music import parse_library_xml
from io import StringIO
from models import LibraryData  # Assuming you have a LibraryData model like for COLLECTION

# Sample XML content for testing the library parsing
SAMPLE_LIBRARY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <dict>
        <key>Tracks</key>
        <dict>
            <key>1</key>
            <dict>
                <key>Name</key><string>Test Track 1</string>
                <key>Artist</key><string>Test Artist 1</string>
                <key>Album</key><string>Test Album 1</string>
                <key>Location</key><string>file://test/location/track1.mp3</string>
                <key>Bit Rate</key><integer>320</integer>
                <key>Total Time</key><integer>300</integer>
            </dict>
            <key>2</key>
            <dict>
                <key>Name</key><string>Test Track 2</string>
                <key>Artist</key><string>Test Artist 2</string>
                <key>Album</key><string>Test Album 2</string>
                <key>Location</key><string>file://test/location/track2.mp3</string>
                <key>Bit Rate</key><integer>256</integer>
                <key>Total Time</key><integer>240</integer>
            </dict>
        </dict>
    </dict>
    <dict>
        <key>Playlists</key>
        <array>
            <dict>
                <key>Name</key><string>Test Playlist 1</string>
                <array>
                    <dict>
                        <key>Track ID</key><integer>1</integer>
                    </dict>
                </array>
            </dict>
            <dict>
                <key>Name</key><string>Test Playlist 2</string>
                <array>
                    <dict>
                        <key>Track ID</key><integer>2</integer>
                    </dict>
                </array>
            </dict>
        </array>
    </dict>
</root>
"""


def test_parse_library_xml():
    # Use StringIO to simulate a file-like object for the XML content
    xml_file = StringIO(SAMPLE_LIBRARY_XML)

    # Call the parsing function
    result = parse_library_xml(xml_file)

    # Validate that the result contains a 'tracks' and 'playlists' key
    assert 'tracks' in result
    assert 'playlists' in result

    # Validate the number of tracks parsed
    assert len(result['tracks']) == 2

    # Validate the first track
    track1 = result['tracks'][0]
    assert track1['track_id'] == "1"
    assert track1['name'] == "Test Track 1"
    assert track1['artist'] == "Test Artist 1"
    assert track1['album'] == "Test Album 1"
    assert track1['location'] == "file://test/location/track1.mp3"
    assert track1['bitrate'] == 320
    assert track1['duration'] == 300

    # Validate the second track
    track2 = result['tracks'][1]
    assert track2['track_id'] == "2"
    assert track2['name'] == "Test Track 2"
    assert track2['artist'] == "Test Artist 2"
    assert track2['album'] == "Test Album 2"
    assert track2['location'] == "file://test/location/track2.mp3"
    assert track2['bitrate'] == 256
    assert track2['duration'] == 240

    # Validate the number of playlists parsed
    assert len(result['playlists']) == 2

    # Validate the first playlist
    playlist1 = result['playlists'][0]
    assert playlist1['playlist_name'] == "Test Playlist 1"
    assert len(playlist1['tracks']) == 0  # No track mapping logic in the provided parser

    # Validate the second playlist
    playlist2 = result['playlists'][1]
    assert playlist2['playlist_name'] == "Test Playlist 2"
    assert len(playlist2['tracks']) == 0  # No track mapping logic in the provided parser
