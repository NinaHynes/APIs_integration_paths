from fastapi import FastAPI, HTTPException
from models import LibraryData
from parse_rekordbox import parse_rekordbox_xml
from parse_traktor import parse_collection_nml
from parse_apple_music import parse_library_xml
import os

app = FastAPI(debug=True, reload=True)


@app.get("/parse-file", response_model=LibraryData)
async def parse_file(file_path: str, file_type: str):
    """
    Parses the file at the given file path based on the file type.
    
    :param file_path: Path to the file on the system.
    :param file_type: Type of file ('rekordbox', 'traktor', 'apple_music').
    :return: Parsed data as LibraryData.
    """
    # Print the file path to confirm what FastAPI is receiving
    print(f"Received file path: {file_path}")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found at: {file_path}")
        raise HTTPException(status_code=404, detail="File not found.")

    # Test opening the file
    try:
        with open(file_path, 'r') as file:
            print("File opened successfully!")
    except Exception as e:
        print(f"Error opening file: {e}")
        raise HTTPException(status_code=500, detail=f"Error opening file: {e}")

    # Parse based on the file type
    try:
        if file_type == "rekordbox":
            if not file_path.endswith('.xml'):
                raise HTTPException(status_code=400, detail="Rekordbox file must be XML.")
            # Pass the file path directly to the parser function
            print("Parsing Rekordbox XML file.")
            return parse_rekordbox_xml(file_path)
        
        elif file_type == "traktor":
            if not file_path.endswith('.nml'):
                raise HTTPException(status_code=400, detail="Traktor file must be NML.")
            with open(file_path, 'r') as file:
                print("Opening Collection NML file.")
                return parse_collection_nml(file)

        elif file_type == "apple_music":
            if not file_path.endswith('.xml'):
                raise HTTPException(status_code=400, detail="Music app file must be XML.")
            with open(file_path, 'r') as file:
                print("Opening Library XML file.")
                return parse_library_xml(file)
        
        else:
            raise HTTPException(status_code=400, detail="Invalid file type. Choose from 'rekordbox', 'traktor' or 'apple_music'.")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
