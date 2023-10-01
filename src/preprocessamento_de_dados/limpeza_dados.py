# import libraries
import pandas as pd
import numpy as np
import re

# /bimtra: lista de dicionarios com: "flightid", "origem", "destino", "dt_dep", "dt_arr"
# flightid: string - unique id
# origen: string (4 letters) - city
# destino: string (4 letters) - city
# dt_dep: int (possibly alter to datetime)-  departure time
# dt_arr: int (possibly alter to datetime) - arrival time


# /esperas: lista de dicionarios com: "esperas", "hora", "aero"
# esperas: int - esperas por hora
# hora: int (possibly alter to datetime)
# aero: string (4 letters) - city

# /satelite: lista de dicionarios com: "data", "path", "tamanho"
# exemplo:
# [
#   {
#     "data": "2022-06-01 01:00:00",
#     "path": "http://satelite.cptec.inpe.br/repositoriogoes/goes16/goes16_web/ams_ret_ch11_baixa/2022/06/S11635384_202206010100.jpg",
#     "tamanho": 1879673
#   },
#   {
#     "data": "2022-06-01 02:00:00",
#     "path": "http://satelite.cptec.inpe.br/repositoriogoes/goes16/goes16_web/ams_ret_ch11_baixa/2022/06/S11635384_202206010200.jpg",
#     "tamanho": 1877693
#   }
# ]
# data: datetime hourly data
# path: string url to satelite data 24 * 365 = 8760 images
# tamanho: int (find out what it means)


# /metaf: lista de dicionarios com: "hora", "metaf", "aero"
# exemplo:
# [
#   {
#     "hora": 1654041600000,
#     "metaf": "METAF SBGL 010000Z  25002KT 3000     BR OVC033   23/21 Q1016=\n",
#     "aero": "SBGL"
#   },
#   {
#     "hora": 1654045200000,
#     "metaf": "METAF SBGL 010100Z 02001KT 2000     BR OVC011   22/21 Q1017=\n",
#     "aero": "SBGL"
#   }
# ]
# descobrir o que metaf quer dizer

# /metar: lista de dicionarios com: "hora", "metar", "aero"
# exemplo:
# [
#   {
#     "hora": 1654041600000,
#     "metar": "METAR SBBR 010000Z 07002KT CAVOK 21/08 Q1018=",
#     "aero": "SBBR"
#   },
#   {
#     "hora": 1654045200000,
#     "metar": "METAR SBBR 010100Z 10002KT CAVOK 20/09 Q1019=",
#     "aero": "SBBR"
#   }
# ]


# /tc-prev: lista de dicionarios com: "hora", "troca", "aero"
# exemplo:
# [
#   {
#     "hora": 1654041600000,
#     "troca": 0,
#     "aero": "BR"
#   },
#   {
#     "hora": 1654045200000,
#     "troca": 0,
#     "aero": "BR"
#   }
# ]

# /tc-real: lista de dicionarios com: "hora", "nova_cabeceira", "antiga_cabeceira", "aero"
# exemplo:
# [
#   {
#     "hora": 1654092843000,
#     "nova_cabeceira": "32",
#     "antiga_cabeceira": "03",
#     "aero": "FL"
#   },
#   {
#     "hora": 1654109470000,
#     "nova_cabeceira": "18",
#     "antiga_cabeceira": "12",
#     "aero": "RF"
#   }
# ]

# /cat-62: so consegui erro 500 (Internal Server Error) - Luiza (2023-09-18)


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
        df = pd.read_csv(file_path, nrows=n, delimiter=',', encoding='utf-8')
        # Return the DataFrame.
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def clean_metaf(array):
    """
    Clean the 'metaf' column of a DataFrame.

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

if __name__ == "__main__":
    # Replace 'your_file.csv' with the path to your CSV file.
    # You can also specify the number of lines to read as the second argument.
    df = read_csv_first_n_entries('../dados.csv', n=5)
    if df is not None:
        df.fillna(0, inplace=True)
        print(df["metaf"])
        df["metaf"] = clean_metaf(df["metaf"])
        print(df["metaf"])