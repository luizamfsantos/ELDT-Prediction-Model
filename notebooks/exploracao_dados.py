# %% [markdown]
# # import libraries

# %%
# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys

# add current directory to system path
sys.path.append(os.getcwd())

# import limpeza_dados
from src.preprocessamento_de_dados.limpeza_dados import *

# %% [markdown]
# ### METAF Data
# - 'hora' data is in miliseconds (hour*3600000)
# - data is hourly
# - there are 4 airports represented
# - data is consistent from day to day

# %% [markdown]
# # daily metaf data for june

# %%
file_path = '../data/processado/metaf/metaf_2022-06-01_2022-06-30.csv'
metaf_june_2022 = pd.read_csv(file_path)
metaf_june_2022.head()
# cws = os.getcwd()
# print(cws)

# %% [markdown]
# ### metaf_june_2022 columns
# METAF has 4 columns: hora, metaf, aero, hora_dt

# %%
metaf_june_2022.dtypes

# %% [markdown]
# ### hora_dt column

# %%
metaf_june_2022["hora_dt"] = pd.to_datetime(metaf_june_2022["hora_dt"])

# %%
metaf_june_2022["hora_dt"].describe()

# %%
# set index [hora_dt, aero]
# metaf_june_2022.set_index(["hora_dt", "aero"], inplace=True)

# %% [markdown]
# ### Metaf column
# CAVOK: Ceiling And Visibility OK

# %% [markdown]
# ### Metaf for airport SBGL

# %%
metaf_june_2022_SBGL = metaf_june_2022[metaf_june_2022["aero"]=="SBGL"].copy()

# %%
from random import randint
from random import seed
# create a list of random integers
seed(1)
randomlist = [randint(0, 100) for i in range(0, 5)]

# %%
metaf_june_2022_SBGL.iloc[randomlist]

# %%
from src.preprocessamento_de_dados.limpeza_dados import *
metaf_june_2022_SBGL=expand_taf_metar(metaf_june_2022_SBGL)

# %%
metaf_june_2022_SBGL.index

# %%
# desired format: METAF,SBGL,25001KT,3000,....
# if after KT, there is not a number, add 0000
# if after KT, there is a number, don't change
for row in metaf_june_2022_SBGL["metaf"]:
    if not row.split("KT,")[1][0].isdigit():
        # if it has CAVOK, then the number is 10000
        if "CAVOK" in row:
            row = row.replace("KT,", "KT,10000,")
        else:
            row = row.replace("KT,", "KT,0000,")
        print(row)

# %%
# string into multiple columns
# columns = ["report", "station", "dt_origin", "wind", "visibility", "weather", "clouds","temperature", "dew_point","altimeter (hPA)"]
new_columns = metaf_june_2022_SBGL["metaf"].str.split(",", expand=True)

# %%
new_columns.shape

# %%
# check whether any of the rows in columns 2 does not end in Z
new_columns[2].str.endswith("Z").value_counts()

# %%
# check whether any of the rows in columns 3 does not end in KT
new_columns[3].str.endswith("KT").value_counts()

# %% [markdown]
# Visibility
# CAVOK: Ceiling And Visibility OK -> replaces visibility, clouds and weather
# 5000 means visibility is 5000 meters.

# %%
new_columns[4].unique()

# %%
multiples_of_1000 = np.arange(1000, 10000, 1000)
multiples_of_1000 = multiples_of_1000.astype(str)

# %%
new_columns[4].isin(multiples_of_1000).value_counts()

# %%
new_columns[~new_columns[4].isin(multiples_of_1000)].head()


