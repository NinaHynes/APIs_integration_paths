import xml.etree.ElementTree as ET
from models import Track, Playlist, LibraryData

def parse_library_xml(file_path: str) -> LibraryData:
    try:
        # Parse the XML file from the provided file path
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Step 1: Extract all tracks and store them in a dictionary
        tracks = {}
        tracks_section = None

        print("Parsing Tracks Section...")
        for dict_elem in root.iter('dict'):
            for key_elem in dict_elem.findall('key'):
                if key_elem.text == "Tracks":
                    tracks_section = dict_elem.find('dict')
                    break
            if tracks_section:
                break

        if tracks_section is not None:
            track_elements = list(tracks_section)
            for i in range(0, len(track_elements), 2):
                track_key_elem = track_elements[i]
                track_data_elem = track_elements[i + 1] if i + 1 < len(track_elements) else None
                track_id = str(track_key_elem.text)  # Convert Track ID to string
                if track_data_elem is not None and track_data_elem.tag == 'dict':
                    track_info = {}
                    for j in range(0, len(track_data_elem), 2):
                        key = track_data_elem[j]
                        value = track_data_elem[j + 1] if j + 1 < len(track_data_elem) else None
                        if key.tag == 'key':
                            key_name = key.text
                            if key_name == "Name":
                                track_info['name'] = value.text
                            elif key_name == "Artist":
                                track_info['artist'] = value.text
                            elif key_name == "Album":
                                track_info['album'] = value.text
                            elif key_name == "Location":
                                track_info['location'] = value.text
                            elif key_name == "Bit Rate":
                                track_info['bitrate'] = int(value.text) if value is not None else None
                            elif key_name == "Total Time":
                                track_info['duration'] = int(value.text) if value is not None else None

                    if track_id and track_info:
                        track_info['track_id'] = track_id
                        tracks[track_id] = Track(
                            track_id=track_id,
                            name=track_info.get('name'),
                            artist=track_info.get('artist'),
                            album=track_info.get('album'),
                            location=track_info.get('location'),
                            bitrate=track_info.get('bitrate'),
                            duration=track_info.get('duration')
                        )

        print("Tracks parsed:", tracks)

        # Step 2: Extract all playlists and link tracks using Track IDs
        playlists = []
        print("Parsing Playlists Section...")
        for dict_elem in root.iter('dict'):
            for key_elem in dict_elem.findall('key'):
                if key_elem.text == "Playlists":
                    playlists_array = dict_elem.find('array')
                    if playlists_array is not None:
                        for playlist_dict in playlists_array.findall('dict'):
                            playlist_name = None
                            playlist_tracks = []

                            # Extract playlist name and track IDs
                            for i in range(0, len(playlist_dict), 2):
                                key = playlist_dict[i]
                                value = playlist_dict[i + 1] if i + 1 < len(playlist_dict) else None

                                if key.tag == 'key' and key.text == "Name":
                                    playlist_name = value.text
                                    print(f"Found Playlist: {playlist_name}")
                                elif key.tag == 'key' and key.text == "Playlist Items":
                                    print(f"Found Playlist Items for {playlist_name}")
                                    track_array = value.find('array')
                                    if track_array is not None:
                                        for track_dict in track_array.findall('dict'):
                                            for k in range(0, len(track_dict), 2):
                                                track_key = track_dict[k]
                                                track_value = track_dict[k + 1] if k + 1 < len(track_dict) else None
                                                if track_key.tag == 'key' and track_key.text == "Track ID":
                                                    track_id = str(track_value.text)  # Convert Track ID to string
                                                    print(f"Track ID in Playlist {playlist_name}: {track_id}")
                                                    if track_id in tracks:
                                                        print(f"Track {track_id} found in Tracks, adding to Playlist {playlist_name}")
                                                        playlist_tracks.append(tracks[track_id])
                                                    else:
                                                        print(f"Track ID {track_id} not found in Tracks!")

                            if playlist_name:
                                playlists.append(Playlist(
                                    playlist_name=playlist_name,
                                    tracks=playlist_tracks
                                ))

        print("Parsed Playlists:", playlists)

        return LibraryData(playlists=playlists, tracks=list(tracks.values()))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise ValueError(f"An error occurred: {str(e)}")
