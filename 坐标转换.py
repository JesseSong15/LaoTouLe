import pandas as pd

def convert_dms_to_decimal(input_csv_path, output_csv_path):
    """
    Converts geographic coordinates from DMS (Degrees, Minutes, Seconds) format to decimal degrees.
    
    Parameters:
        input_csv_path (str): The file path for the input CSV containing the DMS coordinates.
        output_csv_path (str): The file path for the output CSV with the coordinates in decimal degrees.
    """
    def dms_to_dd(dms_str):
        """Convert DMS string to decimal degrees, removing directional symbols."""
        dms_str = dms_str.replace("E", "").replace("N", "").strip()
        try:
            degrees, rest = dms_str.split("°")
            minutes, seconds = rest.split("′")
            degrees = float(degrees)
            minutes = float(minutes) / 60
            seconds = float(seconds.replace('″', '')) / 3600
        except ValueError:  # Handle potential format issues
            return None
        return degrees + minutes + seconds
    
    # Try loading the CSV with UTF-8 first, then GBK if UTF-8 fails
    try:
        data = pd.read_csv(input_csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(input_csv_path, encoding='gbk')
    
    # Apply the conversion
    data['Longitude'] = data['Longitude'].apply(dms_to_dd)
    data['Latitude'] = data['Latitude'].apply(dms_to_dd)
    
    # Check for conversion issues
    if data[['Longitude', 'Latitude']].isnull().any(axis=1).sum() > 0:
        print("Warning: Some rows could not be converted.")
    
    # Save the modified data
    data.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Data converted and saved to {output_csv_path}")

# Example usage
input_csv_path = r'样点数据2.csv'  # Replace with your input CSV file path
output_csv_path = r'样点数据_New.csv'  # Replace with your desired output CSV file path
convert_dms_to_decimal(input_csv_path, output_csv_path)