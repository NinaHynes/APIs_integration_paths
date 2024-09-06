# Test opening the file directly
file_path = "/home/dci-student/Documents/djoid_integrate_APIs/Integrate_APIs_to_kopf/rekordbox/itunes/xml_nml_files/recordbox (orig).xml"

try:
    with open(file_path, 'r') as file:
        print("File opened successfully!")
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
