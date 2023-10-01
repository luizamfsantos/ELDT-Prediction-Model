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
        'wind': ['25002KT', '02001KT'],
        'visibility': [3000, 2000],
        'weather': ['BR', 'BR'],
        'clouds': ['OVC033', 'OVC011'],
        'temperature': ['23/21', '22/21'],
        'dew_point': ['21', '21'],
        'altimeter (hPA)': ['Q1016=', 'Q1017='],
        'aero': ['SBGL', 'SBSG']
    }

    # Create dataframes
    df_error = pd.DataFrame(data_error)
    df_no_error = pd.DataFrame(data_no_error)

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