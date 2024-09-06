import pytest
from parse_library import parse_library_xml
from io import StringIO

# Sample library XML with tracks and playlists that reference track IDs
SAMPLE_LIBRARY_XML_WITH_PLAYLIST_TRACKS = """
<?xml version="1.0" encoding="UTF-8"?>
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
                <key>Playlist Items</key>
                <array>
                    <dict>
                        <key>Track ID</key><integer>1</integer>
                    </dict>
                </array>
            </dict>
            <dict>
                <key>Name</key><string>Test Playlist 2</string>
                <key>Playlist Items</key>
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

def test_parse_library_with_playlist_tracks():
    # Use StringIO to simulate a file-like object for the XML content
    xml_file = StringIO(SAMPLE_LIBRARY_XML_WITH_PLAYLIST_TRACKS)

    # Call the parsing function
    result = parse_library_xml(xml_file)

    # Validate the result has tracks parsed
    assert len(result['tracks']) == 2

    # Validate that playlists are created correctly
    assert len(result['playlists']) == 2

    # Validate the first playlist references the first track
    playlist1 = result['playlists'][0]
    assert playlist1['playlist_name'] == "Test Playlist 1"
    assert len(playlist1['tracks']) == 1
    assert playlist1['tracks'][0]['track_id'] == "1"

    # Validate the second playlist references the second track
    playlist2 = result['playlists'][1]
    assert playlist2['playlist_name'] == "Test Playlist 2"
    assert len(playlist2['tracks']) == 1
    assert playlist2['tracks'][0]['track_id'] == "2"
