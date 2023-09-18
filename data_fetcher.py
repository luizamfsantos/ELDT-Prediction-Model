import requests

# Base de dados
# 1. BIMTRA (Banco de Informações de Movimento de Tráfego Aéreo)
# 2. CAT-62 (Dados de Síntese Radar)
# 3. Esperas (Dados de Quantidades de Esperas em voo por hora)
# 4. METAF (Terminal Aerodrome Forecast)
# 5. METAR (Relatório Meteorológico de Aeródromo)
# 6. Satélite Meteorológico
# 7. Previsão da Troca de Cabeceiras de Aeródromo (tc-prev)
# 8. Histórico da Troca de Cabeceiras de Aeródromo (tc-real)

db = ['bimtra', 'cat-62', 'esperas', 'metaf', 'metar', 'satelite', 'tc-prev', 'tc-real']    # Lista de bases de dados

# Periodo: de junho de 2022 a maio de 2023

# Exemplo de Request URL
# http://montreal.icea.decea.mil.br:5002/api/v1/bimtra?token={VIRTUAL-KEY}&idate=2022-06-01&fdate=2022-06-02

# /bimtra: lista de dicionarios com: "flightid", "origem", "destino", "dt_dep", "dt_arr"
# exemplo:
# [
#   {
#     "flightid": "fcb2bf90345705318213ae1307c0f901",
#     "origem": "SBKP",
#     "destino": "SBRJ",
#     "dt_dep": 1654044297000,
#     "dt_arr": 1654046760000
#   },
#   {
#     "flightid": "c7c5c10716335b048f86d8c52fcba3f2",
#     "origem": "SBGR",
#     "destino": "SBRJ",
#     "dt_dep": 1654045021000,
#     "dt_arr": 1654047173000
#   }
# ]

# /cat-62: so consegui erro 500 (Internal Server Error)

# /esperas: lista de dicionarios com: "esperas", "hora", "aero"
# exemplo:
# [
#   {
#     "esperas": 0,
#     "hora": 1654041600000,
#     "aero": "SBBR"
#   },
#   {
#     "esperas": 0,
#     "hora": 1654045200000,
#     "aero": "SBBR"
#   }
# ]

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

class APIClient:
    def __init__(self, token_file, base_url="http://montreal.icea.decea.mil.br:5002/api/v1"):
        self.base_url = base_url
        self.token = self.load_token(token_file)

    def load_token(self, token_file):
        """
        Load API token from a text file.

        Args:
            token_file (str): The path to the text file containing the API token.

        Returns:
            str: The API token.
        """
        try:
            with open(token_file, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            # Handle the case where the token file is not found
            print("Token file not found.")
            return None

    def make_request(self, db, start_date, end_date, method="GET", params=None, data=None, headers=None):
        """
        Make a request to the REST API with the loaded token, specifying the database and time period.

        Args:
            db (str): The database name you want to access.
            start_date (str): The start date for the time period (e.g., "2022-06-01").
            end_date (str): The end date for the time period (e.g., "2022-06-02").
            method (str): The HTTP method for the request (e.g., GET, POST, PUT, DELETE).
            params (dict): Query parameters to include in the request.
            data (dict): Request body data for POST or PUT requests.
            headers (dict): Additional headers to include in the request.

        Returns:
            dict or int: The JSON response from the API if the status code is 200, else the status code.
        """
        url = f"{self.base_url}/{db}?token={self.token}&idate={start_date}&fdate={end_date}"

        try:
            response = requests.request(
                method,
                url,
                params=params,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
            else:
                return response.status_code
        except requests.exceptions.RequestException as e:
            # Handle exceptions or errors here
            print(f"Request error: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    base_url = "http://montreal.icea.decea.mil.br:5002/api/v1"
    token_file = "../virtual_token.txt"  # MODIFY THIS FOR YOUR TOKEN FILE
    api = APIClient(base_url, token_file)

    # Example GET request for database 'bimtra' and time period '2022-06-01' to '2022-06-02'
    db = 'bimtra'
    start_date = '2022-06-01'
    end_date = '2022-06-02'
    response = api.make_request(db, start_date, end_date)

    if response:
        # Process the response data here
        print(response)