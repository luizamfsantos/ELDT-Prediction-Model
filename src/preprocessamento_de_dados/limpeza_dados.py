# import libraries
import pandas as pd
import numpy as np

def read_csv_first_n_entries(file_path, n=100, delimiter=',', encoding='utf-8'):
    """
    Read the first 'n' entries from a CSV file using Pandas.

    Parameters:
    - file_path (str): The path to the CSV file.
    - n (int, optional): The number of entries to read. Default is 100.

    Returns:
    - DataFrame: A Pandas DataFrame containing the first 'n' entries from the CSV file.
    """
    try:
        # Read the CSV file into a DataFrame, limiting the number of rows to 'n'.
        df = pd.read_csv(file_path, nrows=n, delimiter=delimiter, encoding=encoding)
        # Return the DataFrame.
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def clean_taf_metar(array):
    """
    Clean the 'metaf' or 'metar' column of a DataFrame.

    Parameters:
    - array (array): The 'metaf' column of a DataFrame.
    
    Returns:
    - array: The cleaned 'metaf' column of a DataFrame.
    """
    # Remove space after - 
    array = array.str.replace(r'-\s+', '-', regex=True)

    # Remove =\n
    array = array.str.replace(r'=\n', '', regex=True)

    # Remove spaces at the beginning and end of the string
    array = array.str.strip()

    # Replace multiple spaces with a single comma
    array = array.str.replace(r'\s+', ',', regex=True)

    # Replace / with ,
    array = array.str.replace(r'/', ',', regex=True)
    
    return array

def expand_taf_metar(df, report="metaf"):
    """
    Expand the 'metaf' or 'metar' column of a DataFrame.

    Parameters:
    - df (DataFrame): A DataFrame containing a 'metaf' or 'metar' column.

    Returns:
    - DataFrame: A DataFrame containing the expanded 'metaf' or 'metar' column.
        new columns = ["COR", "AUTO", "NIL", "CAVOK", "report", "station", "dt_origin", "wind", "visibility", "weather", "clouds","temperature", "dew_point","altimeter (hPA)"]
    """

    # check if df contains metaf or metar column
    if ("metaf" not in df.columns) and ("metar" not in df.columns):
        return df
    
    # create columns COR, AUTO, NIL, and CAVOK
    df = add_missing_columns(df,report)
    
    # clean metaf column
    df[report] = clean_taf_metar(df[report])

    # expand metaf column
    # separate report from the rest
    df[["report","rest"]] = df[report].str.split(',', n=1, expand=True)
    check_report(df) # check if df["report"] == "METAF" or df["report"] == "METAR"

    # separate station from the rest
    df[["station","rest"]] = df["rest"].str.split(',', n=1, expand=True)
    check_station(df) # check if station is one of the allowed values
    
    # separate dt_origin from the rest
    df[["dt_origin","rest"]] = df["rest"].str.split(',', n=1, expand=True)
    check_dt_origin(df)
    
    # separate wind from the rest
    df[["wind","rest"]] = df["rest"].str.split(',', n=1, expand=True)
    check_wind(df)

    # check if wind has 2 components 
    df = check_wind_2_components(df)

    # add visibility if missing
    df = check_missing_visibility(df)

    # separate visibility from the rest
    df[["visibility","rest"]] = df["rest"].str.split(',', n=1, expand=True)

    # check whether there is at least one weather phenomena, if not add NaN,
    df = check_missing_phenomena(df)

    # separate weather from the rest
    df[["weather","rest"]] = df["rest"].str.split(',', n=1, expand=True)

    # check if there is any extra phenomena, if so add them to the weather column
    df = check_extra_phenomena(df)
    
    # separate clouds from the rest
    df[["clouds","rest"]] = df["rest"].str.split(',', n=1, expand=True)

    # separate temperature from the rest
    df[["temperature","rest"]] = df["rest"].str.split(',', n=1, expand=True)

    # separate dew_point from altimeter (hPA)
    df[["dew_point","altimeter (hPA)"]] = df["rest"].str.split(',', n=1, expand=True)

    # drop rest and metaf column
    df.drop(columns=["rest",report], inplace=True)

    return df

def add_missing_columns(df, report="metaf"):
    # create columns COR, AUTO, NIL, and CAVOK with 0s
    df["COR"] = 0
    df["AUTO"] = 0
    df["NIL"] = 0
    df["CAVOK"] = 0

    # update columns COR, AUTO, NIL, and CAVOK with 1s if they are present in the metaf column
    df["COR"] = np.where(df[report].str.contains("COR"), 1, df["COR"])
    df["AUTO"] = np.where(df[report].str.contains("AUTO"), 1, df["AUTO"])
    df["NIL"] = np.where(df[report].str.contains("NIL"), 1, df["NIL"])
    df["CAVOK"] = np.where(df[report].str.contains("CAVOK"), 1, df["CAVOK"])

    # remove the words COR, AUTO, NIL from the metaf column
    df[report] = df[report].str.replace("COR", "", regex=False)
    df[report] = df[report].str.replace("AUTO", "", regex=False)
    df[report] = df[report].str.replace("NIL", "", regex=False)

    return df

def check_report(df):
    # Check if all values in df["report"] are equal to "METAF" or "METAR"
    if not (df["report"].isin(["METAF", "METAR"]).all()):
        raise ValueError("Not all values in df['report'] are equal to METAF")

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

def check_wind_2_components(df):
    pattern = r'^(\d{3}V\d{3})'
    mask = df["rest"].str.match(pattern, na=False)
    
    # Create a new DataFrame to store the extracted values
    extracted_values = df.loc[mask, "rest"].str.extract(pattern)
    extracted_values.columns = ["extracted_wind"]
    
    # Update the "wind" and "rest" columns separately
    df.loc[mask, "wind"] = df.loc[mask, "wind"] + " " + extracted_values["extracted_wind"]
    df.loc[mask, "rest"] = df.loc[mask, "rest"].str.replace(pattern + ",", "", regex=True)
    
    return df

def check_missing_visibility(df):
    # check if rest starts with number where rest is the rest of the string after wind
    if ~(df["rest"].str.startswith(r'\d').all()):
        # if the next value is CAVOK, then visibility is 10000 so add 10000, to the beginning of the string
        df["rest"] = np.where(df["rest"].str.startswith("CAVOK"), "10000," + df["rest"], df["rest"])
        # any other case, add 0000, to the beginning of the string
        condition = ~(df["rest"].str.match(r'^\d')) & ~(df["rest"].str.startswith("CAVOK"))
        df["rest"] = np.where(condition, "0000," + df["rest"], df["rest"])
    return df

def check_missing_phenomena(df):
    weather_phenomena = {"BR":"Mist", "FG":"Fog", "HZ":"Haze", "RA":"Rain", "SN":"Snow", "TS":"Thunderstorm", "DZ":"Drizzle", "SH":"Showers", "GR":"Hail", "GS":"Small Hail", "FU":"Smoke", "SA":"Sand", "DU":"Dust", "SQ":"Squall", "FC":"Funnel Cloud", "SS":"Sandstorm", "DS":"Duststorm", "PO":"Dust/Sand Whirls", "PY":"Spray", "VA":"Volcanic Ash", "BC":"Patches", "BL":"Blowing", "DR":"Low Drifting", "FZ":"Freezing", "MI":"Shallow", "PR":"Partial", "VC":"Vicinity"}
    result = []
    for row in df["rest"]:
        if row[:2] in weather_phenomena:
            result.append(row)
        elif row[0] in ["-","+"]:
            result.append(row)
        else:
            result.append("NaN," + row)
    
    # replace the rest column with the result list
    df["rest"] = result
    return df

def check_extra_phenomena(df):
    # check if rest starts with 2 letters and a comma, if so then add those letters to the weather column and remove them from the rest column
    pattern = r'^([A-Z]{2})'
    if (df["rest"].str.match(pattern).any()):
        df["weather"] = np.where(df["rest"].str.match(pattern), df["weather"]+ df["rest"].str.extract(pattern)[0], df["weather"])
        df["rest"] = np.where(df["rest"].str.match(pattern), df["rest"].str.replace(pattern + ",", "", regex=True), df["rest"])
    return df

if __name__ == "__main__":
    df = read_csv_first_n_entries('../dados.csv', n=100)
    if df is not None:
        df.dropna(subset=['metaf'], inplace=True)
        df = expand_taf_metar(df)
        print(df.columns)
        print(df["altimeter (hPA)"])
        