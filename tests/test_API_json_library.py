import pytest
from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)

# Sample XML content for testing the library upload API
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
            </dict>
            <dict>
                <key>Name</key><string>Test Playlist 2</string>
            </dict>
        </array>
    </dict>
</root>
"""

def test_upload_library_xml():
    # Use TestClient to simulate a file upload to the /upload-library endpoint
    files = {'xml_file': ('test_library.xml', SAMPLE_LIBRARY_XML, 'application/xml')}
    
    # Post the sample XML to the endpoint
    response = client.post("/upload-library", files=files)
    
    # Check if the status code is 200 (OK)
    assert response.status_code == 200
    
    # Check the response JSON structure
    json_response = response.json()
    
    # Validate the tracks in the response
    assert len(json_response['tracks']) == 2
    track1 = json_response['tracks'][0]
    assert track1['track_id'] == "1"
    assert track1['name'] == "Test Track 1"
    assert track1['artist'] == "Test Artist 1"
    assert track1['album'] == "Test Album 1"
    assert track1['location'] == "file://test/location/track1.mp3"
    assert track1['bitrate'] == 320
    assert track1['duration'] == 300

    track2 = json_response['tracks'][1]
    assert track2['track_id'] == "2"
    assert track2['name'] == "Test Track 2"
    assert track2['artist'] == "Test Artist 2"
    assert track2['album'] == "Test Album 2"
    assert track2['location'] == "file://test/location/track2.mp3"
    assert track2['bitrate'] == 256
    assert track2['duration'] == 240

    # Validate the playlists in the response
    assert len(json_response['playlists']) == 2
    playlist1 = json_response['playlists'][0]
    assert playlist1['playlist_name'] == "Test Playlist 1"
    assert len(playlist1['tracks']) == 0  # No tracks in this test case

    playlist2 = json_response['playlists'][1]
    assert playlist2['playlist_name'] == "Test Playlist 2"
    assert len(playlist2['tracks']) == 0  # No tracks in this test case
