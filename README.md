

## Project Overview

### Initial Approach

This project initially used a **Flask** application to parse the XML and NML files into JSON format. The main goal was to extract key data like **tracks** and **playlists** and return this information in a JSON structure. Parsing was handled using Python’s `xml.etree.ElementTree`, and there was limited validation of the data.

### Transition to FastAPI with Pydantic

We later transitioned the project to **FastAPI** for improved performance and more structured data handling. Using **Pydantic** models, we ensured that the JSON output was consistent and strictly validated. This approach allows us to handle more complex data transformations, including ensuring uniform JSON responses for both **tracks** and **playlists**.

Key improvements:
- **Asynchronous support** via FastAPI.
- **Data validation** using Pydantic models.
- **Uniform JSON output** for all endpoints (e.g., Rekordbox, Collection NML, and Library XML).
- Better handling of different file formats and edge cases.

### JSON Structure

The response JSON structure includes:

- **Tracks**: Metadata related to tracks (e.g., title, artist, album, location, etc.).
- **Playlists**: Playlists that contain references to tracks, ensuring consistency and relationships between the two.

### Endpoints

The API exposes endpoints to upload and parse files:
- `/upload-rekordbox`: Parse Rekordbox XML files to JSON.
- `/upload-collection`: Parse Collection NML files to JSON.
- `/upload-library`: Parse Library XML files to JSON.


