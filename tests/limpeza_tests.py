import pandas as pd
import sys
import os

# Get the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory (root) of the current directory
project_root = os.path.dirname(current_dir)

# Add the project root directory to sys.path
sys.path.append(project_root)

# Import the function to be tested
from src.preprocessamento_de_dados.limpeza_dados import *

if __name__ == "__main__":
    # Sample data for the dataframe that won't raise an error
    data_no_error = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAF', 'METAF'],
        'station': ['SBBR', 'SBCF'],  # These station codes are in the 'aero' dictionary
        'dt_origin': ['010000Z', '010100Z'],
        'wind': ['25002KT', '02001KT'],
        'visibility': [3000, 2000],
        'weather': ['BR', 'BR'],
        'clouds': ['OVC033', 'OVC011'],
        'temperature': ['23/21', '22/21'],
        'dew_point': ['21', '21'],
        'altimeter (hPA)': ['Q1016=', 'Q1017='],
        'aero': ['SBGL', 'SBSG']
    }

    # Sample data for the dataframe that will raise an error
    data_error = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAF'],
        'station': ['XYZ', 'ABC'],  # These station codes are not in the 'aero' dictionary
        'dt_origin': ['010000', '010100Z'],
        'wind': ['25002', '02001KT'],
        'visibility': [3000, 2000],
        'weather': ['BR', 'BR'],
        'clouds': ['OVC033', 'OVC011'],
        'temperature': ['23/21', '22/21'],
        'dew_point': ['21', '21'],
        'altimeter (hPA)': ['Q1016=', 'Q1017='],
        'aero': ['SBGL', 'SBSG']
    }

    data_missing_visibility = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAF'],
        'station': ['XYZ', 'ABC'],  # These station codes are not in the 'aero' dictionary
        'dt_origin': ['010000', '010100Z'],
        'wind': ['25002', '02001KT'],
        'rest': ['BROVC03323/21Q1016', '2000']
    }

    data_CAVOK = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAF'],
        'station': ['XYZ', 'ABC'],  # These station codes are not in the 'aero' dictionary
        'dt_origin': ['010000', '010100Z'],
        'wind': ['25002', '02001KT'],
        'rest': ['CAVOK23/21Q1016', '2000']
    }

    data_missing_phenomena = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAF'],
        'station': ['XYZ', 'ABC'],  # These station codes are not in the 'aero' dictionary
        'dt_origin': ['010000', '010100Z'],
        'wind': ['25002', '02001KT'],
        'visibility': [3000, 2000],
        'rest': ['CAVOK,23/21,Q1016', 'BR,OVC21,23/21,Q1016']
    }

    # Create dataframes
    df_error = pd.DataFrame(data_error)
    df_no_error = pd.DataFrame(data_no_error)
    df_missing_visibility = pd.DataFrame(data_missing_visibility)
    df_CAVOK = pd.DataFrame(data_CAVOK)
    df_missing_phenomena = pd.DataFrame(data_missing_phenomena)

    # Check if the function check_station raises an error
    try:
        check_station(df_error)
    except ValueError:
        print("check_station(df_error) passed")
    else:
        print("check_station(df_error) failed")

    # Check if the function check_station doesn't raise an error
    try:
        check_station(df_no_error)
    except ValueError:
        print("check_station(df_no_error) failed")
    else:
        print("check_station(df_no_error) passed")
    
    # Check if the function check_report raises an error
    try:
        check_report(df_error)
    except ValueError:
        print("check_report(df_error) passed")
    else:
        print("check_report(df_error) failed")
    
    # Check if the function check_report doesn't raise an error
    try:
        check_report(df_no_error)
    except ValueError:
        print("check_report(df_no_error) failed")
    else:
        print("check_report(df_no_error) passed")
    
    # Check if the function check_dt_origin raises an error
    try:
        check_dt_origin(df_error)
    except ValueError:
        print("check_dt_origin(df_error) passed")
    else:
        print("check_dt_origin(df_error) failed")
    
    # Check if the function check_dt_origin doesn't raise an error
    try:
        check_dt_origin(df_no_error)
    except ValueError:
        print("check_dt_origin(df_no_error) failed")
    else:
        print("check_dt_origin(df_no_error) passed")

    # Check if the function check_wind raises an error
    try:
        check_wind(df_error)
    except ValueError:
        print("check_wind(df_error) passed")
    else:
        print("check_wind(df_error) failed")
    
    # Check if the function check_wind doesn't raise an error
    try:
        check_wind(df_no_error)
    except ValueError:
        print("check_wind(df_no_error) failed")
    else:
        print("check_wind(df_no_error) passed")

    # Check if the function check_missing_visibility adds 0000, to the beginning of the string
    if (check_missing_visibility(df_missing_visibility)["rest"].str.startswith("0000,")).any():
        print("check_missing_visibility(df_missing_visibility) passed")
    else:
        print("check_missing_visibility(df_missing_visibility) failed")

    # Check if the function check_missing_visibility adds 10000, to the beginning of the string
    if (check_missing_visibility(df_CAVOK)["rest"].str.startswith("10000,")).any():
        print("check_missing_visibility(df_CAVOK) passed")
    else:
        print("check_missing_visibility(df_CAVOK) failed")
    
    if check_missing_phenomena(df_missing_phenomena)["rest"].str.strip().str.startswith("NaN,").any():
        print("check_missing_phenomena(df_missing_phenomena) passed")
    else:
        print("check_missing_phenomena(df_missing_phenomena) failed")