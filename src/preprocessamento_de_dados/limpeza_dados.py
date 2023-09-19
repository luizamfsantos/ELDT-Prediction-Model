# import libraries
import pandas as pd
import numpy as np

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
# flightid: string - unique id
# origen: string (4 letters) - city
# destino: string (4 letters) - city
# dt_dep: int (possibly alter to datetime)-  departure time
# dt_arr: int (possibly alter to datetime) - arrival time

# /cat-62: so consegui erro 500 (Internal Server Error) - Luiza (2023-09-18)

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