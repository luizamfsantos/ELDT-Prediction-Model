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


def check_report(df):
    # Check if all values in df["report"] are equal to "METAF"
    if not (df["report"] == "METAF").all():
        raise ValueError("Not all values in df['report'] are equal to METAF")

def check_phenomena(value, weather_phenomena):
    if value[:2] in weather_phenomena:
        return value
    else:
        return "NaN," + value
    
def check_station(df):
    aero = {"SBBR":"Brasilia", "SBCF":"Confins", "SBCT":"Curitiba", "SBFL":"Florianopolis", "SBGL":"Rio de Janeiro - Galeao", "SBGR":"Guarulhos", "SBKP":"Campinas", "SBPA":"Porto Alegre", "SBRF":"Recife", "SBRJ":"Rio de Janeiro - Santos Dumont", "SBSP":"Sao Paulo - Congonhas", "SBSV":"Salvador"}
    aero_list = [*aero.keys()]
    if ~(df["station"].isin(aero_list).any()):
        raise ValueError("df['station'] not in aero.keys()")
    
def check_dt_origin(df):
    # check if dt_origin ends with Z
    if ~(df["dt_origin"].str.endswith("Z").all()):
        raise ValueError("df['dt_origin'] is not a valid dt_origin: correct format is day hour minute Z")

def check_wind(df):
    # check if wind ends with KT
    if ~(df["wind"].str.endswith("KT").all()):
        raise ValueError("df['wind'] does not end with KT")

def check_missing_visibility(df):
    # check if rest starts with number where rest is the rest of the string after wind
    if ~(df["rest"].str.startswith(r'\d').all()):
        # if the next value is CAVOK, then visibility is 10000 so add 10000, to the beginning of the string
        df["rest"] = np.where(df["rest"].str.startswith("CAVOK"), "10000," + df["rest"], df["rest"])
        # any other case, add 0000, to the beginning of the string
        condition = ~(df["rest"].str.match(r'^\d')) & ~(df["rest"].str.startswith("CAVOK"))
        df["rest"] = np.where(condition, "0000," + df["rest"], df["rest"])
    return df

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

    # Create dataframes
    df_error = pd.DataFrame(data_error)
    df_no_error = pd.DataFrame(data_no_error)
    df_missing_visibility = pd.DataFrame(data_missing_visibility)
    df_CAVOK = pd.DataFrame(data_CAVOK)

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