import pandas as pd

# metaf_2022_06_02 = pd.read_csv('../../data/bruto/metaf/metaf_2022-06-02_2022-06-02.csv')
# metaf_2022_06_02["hora_dt"] = metaf_2022_06_02["hora"].apply(lambda x: pd.to_datetime(x, unit='ms'))

# metaf_2022_06_03 = pd.read_csv('../../data/bruto/metaf/metaf_2022-06-03_2022-06-03.csv')
# metaf_2022_06_03["hora_dt"] = metaf_2022_06_03["hora"].apply(lambda x: pd.to_datetime(x, unit='ms'))

# combined_metaf = pd.concat([metaf_2022_06_02, metaf_2022_06_03], ignore_index=True)

# Initialize an empty dataframe to store the combined data
combined_metaf = pd.DataFrame()

# Define the start and end dates for June
start_date = pd.to_datetime('2022-06-01')
end_date = pd.to_datetime('2022-06-30')

# Loop through each day in June
current_date = start_date
while current_date <= end_date:
    # Generate the file path for the current day
    file_path = f'data/bruto/metaf/metaf_{current_date.strftime("%Y-%m-%d")}_{current_date.strftime("%Y-%m-%d")}.csv'
    
    # Read the data for the current day
    try: 
        current_data = pd.read_csv(file_path)
    except FileNotFoundError:
        current_date += pd.Timedelta(days=1)
        continue

    # Convert the 'hora' column to datetime
    current_data["hora_dt"] = current_data["hora"].apply(lambda x: pd.to_datetime(x, unit='ms'))
    
    # Concatenate the current day's data to the combined dataframe
    combined_metaf = pd.concat([combined_metaf, current_data], ignore_index=True)
    
    # Move to the next day
    current_date += pd.Timedelta(days=1)

# Now, combined_metaf contains the data for all days in June 2022
combined_metaf.to_csv('data/processado/metaf/metaf_2022-06-01_2022-06-30.csv', index=False)