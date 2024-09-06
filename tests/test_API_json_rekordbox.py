import pytest
from fastapi.testclient import TestClient
from app import app  

client = TestClient(app)  # Initialize the TestClient for API tests

def test_missing_playlists():
    # Mocked XML without any playlists
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <root>
        <COLLECTION>
            <TRACK TrackID="1" Name="Test Track" Location="file://test/location/track.mp3" />
        </COLLECTION>
    </root>"""
    
    # Simulate file upload
    files = {'xml_file': ('test.xml', xml_content, 'application/xml')}
    
    # Call the FastAPI endpoint
    response = client.post("/upload-rekordbox", files=files)
    
    # Ensure the response code is 200 (OK)
    assert response.status_code == 200
    
    # Extract the JSON response
    json_response = response.json()
    
    # Ensure no playlists are returned
    assert len(json_response['playlists']) == 0

def test_track_parsing():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <DJ_PLAYLISTS>
        <COLLECTION>
            <TRACK TrackID="47468967" Name="NOISE" Location="file://localhost/test.mp3" BitRate="320" />
        </COLLECTION>
    </DJ_PLAYLISTS>"""
    
    files = {'xml_file': ('test.xml', xml_content, 'application/xml')}
    response = client.post("/upload-rekordbox", files=files)
    
    # Ensure the response code is 200 (OK)
    assert response.status_code == 200
    
    # Extract the JSON response
    json_response = response.json()
    
    # Validate track details
    assert json_response['tracks'][0]['track_id'] == "47468967"
    assert json_response['tracks'][0]['name'] == "NOISE"
    assert json_response['tracks'][0]['location'] == "file://localhost/test.mp3"
    assert json_response['tracks'][0]['bitrate'] == 320
