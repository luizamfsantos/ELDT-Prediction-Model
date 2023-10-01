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
        'weather': ['BR', '-PA'],
        'clouds': ['OVC033', 'OVC011'],
        'temperature': ['23/21', '22/21'],
        'dew_point': ['21', '21'],
        'altimeter (hPA)': ['Q1016=', 'Q1017='],
        'aero': ['SBGL', 'SBSG']
    }

    # Sample data for the dataframe that will raise an error
    data_error = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAD', 'METAF'],
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

    data_wind_2_components = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAF'],
        'station': ['XYZ', 'ABC'],  # These station codes are not in the 'aero' dictionary
        'dt_origin': ['010000', '010100Z'],
        'wind': ['25002', '02001KT'],
        'rest': ['BROVC03323/21Q1016', '050V160,2000']
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
        'station': ['XYZ', 'ABC'],  
        'dt_origin': ['010000', '010100Z'],
        'wind': ['25002', '02001KT'],
        'visibility': [3000, 2000],
        'rest': ['CAVOK,23/21,Q1016', 'BR,OVC21,23/21,Q1016']
    }

    data_with_phenomena = {
        'hora': [1654041600000, 1654045200000],
        'report': ['METAR', 'METAF'],
        'station': ['XYZ', 'ABC'],  
        'dt_origin': ['010000', '010100Z'],
        'wind': ['25002', '02001KT'],
        'visibility': [3000, 2000],
        'rest': ['-PA,OVC22,23/21,Q1016', 'BR,OVC21,23/21,Q1016']
    }

    data_METAR_raw = [
        [1654174800000, "METAR SBBR 021300Z 07006KT 030V090 CAVOK 23/11 Q1021=", "SBBR", "2022-06-02 13:00:00"],
        [1654178400000, "METAR SBBR 021400Z 07004KT 010V120 CAVOK 25/12 Q1021=", "SBBR", "2022-06-02 14:00:00"],
        [1654182000000, "METAR SBBR 021500Z 35004KT 290V090 CAVOK 27/11 Q1020=", "SBBR", "2022-06-02 15:00:00"],
        [1654185600000, "METAR SBBR 021600Z 30005KT CAVOK 28/09 Q1019=", "SBBR", "2022-06-02 16:00:00"],
        [1654189200000, "METAR SBBR 021700Z 19006KT 130V230 9999 FEW040 28/10 Q1018=", "SBBR", "2022-06-02 17:00:00"],
        [1654182000000, "METAR SBCT 021500Z VRB02KT 5000 -RA BKN014 OVC050 14/14 Q1019=", "SBCT", "2022-06-02 15:00:00"],
        [1654185600000, "METAR COR SBCT 021600Z 17003KT 6000 -RA BKN012 OVC050 14/14 Q1018=", "SBCT", "2022-06-02 16:00:00"],
        [1654095600000, "METAR SBCF 011500Z 12007KT 060V210 9999 FEW030 25/16 Q1019=", "SBCF", "2022-06-01 15:00:00"],
        [1654099200000, "METAR SBCF 011600Z 09005KT 030V170 9999 FEW035 26/16 Q1018=", "SBCF", "2022-06-01 16:00:00"]
    ]

    columns_METAR_raw = ["hora", "metar", "aero", "hora_dt"]

    # Create dataframes
    df_error = pd.DataFrame(data_error)
    df_no_error = pd.DataFrame(data_no_error)
    df_missing_visibility = pd.DataFrame(data_missing_visibility)
    df_wind_2_components = pd.DataFrame(data_wind_2_components)
    df_CAVOK = pd.DataFrame(data_CAVOK)
    df_missing_phenomena = pd.DataFrame(data_missing_phenomena)
    df_with_phenomena = pd.DataFrame(data_with_phenomena)
    df_METAR_raw = pd.DataFrame(data_METAR_raw, columns=columns_METAR_raw)
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
    
    # Check if the function check_missing_phenomena adds NaN, to the beginning of the string
    if check_missing_phenomena(df_missing_phenomena)["rest"].str.strip().str.startswith("NaN,").any():
        print("check_missing_phenomena(df_missing_phenomena) passed")
    else:
        print("check_missing_phenomena(df_missing_phenomena) failed")
    
    # Check if the function check_missing_phenomena doesn't add NaN, to the beginning of the string on the 2 cases
    if check_missing_phenomena(df_with_phenomena)["rest"].str.strip().str.startswith("NaN,").any():
        print("check_missing_phenomena(df_no_error) failed")
    else:
        print("check_missing_phenomena(df_no_error) passed")

    # Check if the function add_missing_columns adds the columns COR, AUTO, NIL, and CAVOK
    missing_cols = ["COR", "AUTO", "NIL", "CAVOK"]
    for col in missing_cols:
        if col in add_missing_columns(df_METAR_raw,"metar").columns:
            print(f"add_missing_columns(df_no_error) add column {col} passed")
        else:
            print(f"add_missing_columns(df_no_error) add column {col} failed")
    
    # Check if the function add_missing_columns removes words COR, AUTO, NIL from the metar column
    drop_words = ["COR", "AUTO", "NIL"]
    for word in drop_words:
        if not (add_missing_columns(df_METAR_raw,"metar")["metar"].str.contains(word)).any():
            print(f"add_missing_columns(df_no_error) remove {word} passed")
        else:
            print(f"add_missing_columns(df_no_error) remove {word} failed")
    
    # Check if clean_taf_metar function can clean METAR and METAF
    if clean_taf_metar(df_METAR_raw["metar"]).str.startswith("METAR").all():
        print("clean_taf_metar(df_METAR_raw) passed")
    else:
        print("clean_taf_metar(df_METAR_raw) failed")
    
    # Check if check_wind_2_components function adds 060V130 to the wind column
    pattern = r'(\d{3}V\d{3})$'
    result = check_wind_2_components(df_wind_2_components)["wind"]
    if result.str.extract(pattern).any().any():
        print("check_wind_2_components(df_wind_2_components) passed")
    else:
        print(check_wind_2_components(df_wind_2_components)["wind"])
        print(check_wind_2_components(df_wind_2_components)["rest"])
        print("check_wind_2_components(df_wind_2_components) failed")