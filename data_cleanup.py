import pandas as pd

df = pd.read_csv('data.csv')

# month column contains date in the format YYYY-MM
# separate the year and month into two columns
df['year'] = df['month'].apply(lambda x: x.split('-')[0])
df['month'] = df['month'].apply(lambda x: x.split('-')[1])

# convert year and month columns to numeric
df['year'] = pd.to_numeric(df['year'])
df['month'] = pd.to_numeric(df['month'])

# replace values in town column
# replace "CENTRAL AREA" with "RIVER VALLEY"
df['town'] = df['town'].replace('CENTRAL AREA', 'RIVER VALLEY')

# save the dataframe to a new csv file
df.to_csv('data_modified.csv', index=False)