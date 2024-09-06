import pytest
from fastapi.testclient import TestClient
from app import app  

client = TestClient(app)

def test_upload_collection_nml():
    nml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <NML VERSION="19">
        <COLLECTION>
            <ENTRY AUDIO_ID="1" TITLE="Test Track 1" ARTIST="Test Artist 1">
                <LOCATION FILE="file://test/location/track1.mp3" />
                <INFO BITRATE="320" PLAYTIME="300" />
            </ENTRY>
        </COLLECTION>
        <PLAYLISTS>
            <NODE NAME="Test Playlist 1" TYPE="PLAYLIST">
                <ENTRY AUDIO_ID="1" />
            </NODE>
        </PLAYLISTS>
    </NML>
    """
    
    files = {'xml_file': ('test.nml', nml_content, 'application/xml')}
    
    response = client.post("/upload-collection", files=files)
    
    # Check response status
    assert response.status_code == 200
    
    # Check the response JSON
    json_response = response.json()
    assert len(json_response['tracks']) == 1
    assert json_response['tracks'][0]['name'] == "Test Track 1"
    assert len(json_response['playlists']) == 1
    assert json_response['playlists'][0]['playlist_name'] == "Test Playlist 1"
