"""
Author: Caitlin Hanrahan
ICTPRG440 Assignment: Task 2 Write Code
"""

import geopandas as gpd

FILE_PATH = r"spatial_data_original\NPWS_Lookout.shp"
# FILE_PATH = r"spatial_data_original\_.txt"
OUTPUT_FOLDER_PATH = r"output"

def read_to_geodataframe(FilePath):
    
    """
    Defines a function to read vector spatial data and return a geodataframe object.

    Parameters:
    - filepath (str): path to the vector file (e.g. .shp, .geojson etc.)
    Returns:
    - Geodataframe (GeoDataFrame) or None 
    """

    # Ensure valid filepath
    if not isinstance(FilePath, str):
        raise TypeError("\n\n ERROR: filepath is not a string\n\n ")

    # Read shapefile to a geodataframe
    try:
        GeoDataframe = gpd.read_file(FilePath)

    except Exception as e:
        print("\n\n read_to_geodataframe() function error", e, "\n\n")
        GeoDataframe = None

    return GeoDataframe # ---returns geodataframe object

def print_geodataframe(GeoDataframe):
    
    """
    Defines a function to show vector spatial data, attribute table, row by row in the console.

    Parameters:
    - Input geodataframe (GeoDataFrame)
    Returns:
    - None
    """

    # Ensure valid geodataframe
    if not isinstance(GeoDataframe, gpd.GeoDataFrame):
        raise TypeError("\n\n ERROR: geodataframe is not valid\n\n ")

    # Iterate through geodataframe rows one-by-one, prompting user to continue to print each row
    try:
        for index, row in GeoDataframe.iterrows():
            print(f"Row {index}:")
            print(row)
            print("-" * 40)

            prompt = input("next row? (y/n): ")
            if prompt != 'y':
                break

    except Exception as e:
        print("\n\n print_geodataframe() function error", e, "\n\n")

    return None

def project_gcs_to_pcs(InputGDF, OutputFolderPath, ESPG=3308):

    """
    Defines a function to project vector spatial data from geographic coordinate system to a 
    desired projected coordinate system (for example from WGS84 To GDA2020 MGA Z56) 
    and save the output (projected layer) as shapefile to the output folder in the repository.
    
    Parameters:
    - Input geodataframe (GeoDataFrame)
    - OutputFolderPath (str): path to the output folder
    - ESPG (int): desired projected coordinate system espg code. Default 7855 (GDA2020/NSW Lambert)
    Returns:
    - None
    """

    # Print the CRS of the input geodataframe
    try:
        crs = InputGDF.crs
        
        if crs and crs.to_epsg():
            print(f"EPSG: {crs.to_epsg()} - {crs.name}")
        else:
            raise ValueError(f"\n\n input geodataframe CRS not in EPSG format: {crs}\n\n ")
        
    except Exception as e:
        print(f"\n\n Error reading file: {e}\n\n ")

    # Ensure valid input ESPG code
    if not isinstance(ESPG, int):
        raise TypeError("\n\n ERROR: ESPG is not an integer code\n\n ") 

    # Transform and print the CRS of the output geodataframe
    try:
        OutputGDB = InputGDF.to_crs(epsg=ESPG)
        crs = OutputGDB.crs
        
        if crs and crs.to_epsg():
            print(f"EPSG: {crs.to_epsg()} - {crs.name}")
        else:
            raise ValueError(f"\n\n output geodataframe CRS not in EPSG format: {crs}\n\n ")
        
    except Exception as e:
        print("\n\n project_gcs_to_pcs() function error", e, "\n\n")

    # Ensure valid output folder path
    if not isinstance(OutputFolderPath, str):
        raise TypeError("ERROR: output folder path is not a string") 

    # Export output geodataframe to shapefile
    OutputPath = OutputFolderPath + "\\" + "output.shp"
    OutputGDB.to_file(OutputPath, driver="ESRI Shapefile")

    return None

if __name__ == "__main__":

    gdf = read_to_geodataframe(FILE_PATH)
    print_geodataframe(gdf)
    project_gcs_to_pcs(gdf, OUTPUT_FOLDER_PATH)
