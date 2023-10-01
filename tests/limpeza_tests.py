import pandas as pd
import os

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the working directory to the project root
project_root = os.path.abspath(os.path.join(script_dir, '..'))
os.chdir(project_root)

from preprocessamento_de_dados.limpeza_dados import *


def check_report(df):
    # check if df["report"] == "METAF"
    if "METAF" not in df["report"].values:
        ValueError("METAF not found in df['report']")

if __name__ == "__main__":
    data_check_report = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR SBGL 010000Z  25002KT 3000     BR OVC033   23/21 Q1016=', 'METAR SBGL 010100Z 02001KT 2000     BR OVC011   22/21 Q1017='],
        'station': ['SBGL', 'SBGL'],
        'dt_origin': ['010000Z', '010100Z'],
        'wind': ['25002KT', '02001KT'],
        'visibility': [3000, 2000],
        'weather': ['BR', 'BR'],
        'clouds': ['OVC033', 'OVC011'],
        'temperature': ['23/21', '22/21'],
        'dew_point': ['21', '21'],
        'altimeter (hPA)': ['Q1016=', 'Q1017='],
        'aero': ['NaN', 'NaN']
    }
    df_check_report = pd.DataFrame(data_check_report)

