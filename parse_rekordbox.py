import xml.etree.ElementTree as ET
from models import Track, Playlist, LibraryData  # Ensure this import statement is present

def parse_rekordbox_xml(file_path: str) -> LibraryData:
    try:
        print(f"Parsing Rekordbox XML from: {file_path}")
        # Parse the XML file from the provided file path
        tree = ET.parse(file_path)
        root = tree.getroot()

        track_dict = {}
        for track in root.findall(".//COLLECTION/TRACK"):
            print(f"Found track: {track.get('TrackID')}")
            track_id = track.get('TrackID')
            if track_id:
                track_info = Track(
                    track_id=track_id,
                    name=track.get('Name'),
                    artist=track.get('Artist'),
                    album=track.get('Album'),
                    location=track.get('Location'),  # Track location included
                    genre=track.get('Genre'),
                    bitrate=track.get('BitRate'),
                    sample_rate=track.get('SampleRate'),
                    duration=track.get('TotalTime'),
                    bpm=track.get('AverageBpm')
                )
                track_dict[track_id] = track_info

        playlists = []
        playlists_section = root.find(".//PLAYLISTS")
        if playlists_section is not None:
            print("Playlists section found.")
            for node in playlists_section.findall(".//NODE"):
                playlist_name = node.get('Name')

                if playlist_name == "ROOT":
                    continue

                playlist_tracks = []
                for track_node in node.findall(".//TRACK"):
                    track_id = track_node.get('Key')
                    if track_id and track_id in track_dict:
                        print(f"Adding track {track_id} to playlist {playlist_name}")
                        playlist_tracks.append(track_dict[track_id])

                if playlist_tracks:
                    playlists.append(Playlist(
                        playlist_name=playlist_name,
                        tracks=playlist_tracks
                    ))

        print(f"Tracks: {len(track_dict)}, Playlists: {len(playlists)}")
        return LibraryData(playlists=playlists, tracks=list(track_dict.values()))

    except ET.ParseError as parse_error:
        raise ValueError(f"XML Parse Error: {str(parse_error)}")
    except Exception as e:
        print(f"Error in parse_rekordbox_xml: {e}")
        raise ValueError(f"An error occurred: {str(e)}")
