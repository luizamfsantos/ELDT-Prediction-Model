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
    # check if df["report"] == "METAF"
    if "METAF" not in df["report"].values:
        raise ValueError("METAF not found in df['report']")

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

if __name__ == "__main__":
    # data_check_report = {
    #     'hora': [1654041600000, 1654045200000],
    #     'report': ['METAR', 'METAR'],
    #     'station': ['SBGL', 'SBGL'],
    #     'dt_origin': ['010000Z', '010100Z'],
    #     'wind': ['25002KT', '02001KT'],
    #     'visibility': [3000, 2000],
    #     'weather': ['BR', 'BR'],
    #     'clouds': ['OVC033', 'OVC011'],
    #     'temperature': ['23/21', '22/21'],
    #     'dew_point': ['21', '21'],
    #     'altimeter (hPA)': ['Q1016=', 'Q1017='],
    #     'aero': ['SBGL', 'SBSG']}
    # df_check_report = pd.DataFrame(data_check_report)
    # check_report(df_check_report)
    # print("check_report(df_check_report) passed")
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

    # Sample data for the dataframe that won't raise an error
    data_error = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAF'],
        'station': ['XYZ', 'ABC'],  # These station codes are not in the 'aero' dictionary
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

    # Create dataframes
    df_error = pd.DataFrame(data_error)
    df_no_error = pd.DataFrame(data_no_error)

    # Check if the function raises an error
    try:
        check_station(df_error)
    except ValueError:
        print("check_station(df_error) passed")
    else:
        print("check_station(df_error) failed")

    # Check if the function doesn't raise an error

    try:
        check_station(df_no_error)
    except ValueError:
        print("check_station(df_no_error) failed")
    else:
        print("check_station(df_no_error) passed")