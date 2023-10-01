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

if __name__ == "__main__":
    data_check_report = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAR'],
        'station': ['SBGL', 'SBGL'],
        'dt_origin': ['010000Z', '010100Z'],
        'wind': ['25002KT', '02001KT'],
        'visibility': [3000, 2000],
        'weather': ['BR', 'BR'],
        'clouds': ['OVC033', 'OVC011'],
        'temperature': ['23/21', '22/21'],
        'dew_point': ['21', '21'],
        'altimeter (hPA)': ['Q1016=', 'Q1017='],
        'aero': ['SBGL', 'SBSG']}
    df_check_report = pd.DataFrame(data_check_report)
    check_report(df_check_report)
    print("check_report(df_check_report) passed")
