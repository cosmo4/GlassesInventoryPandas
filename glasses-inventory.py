#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd

# Load the Excel file
file_path = 'EV1 Frame inventory.csv'  # Update this path if needed
skip_rows = list(range(11)) + list(range(1686, 2000))

# Read the data into a DataFrame, skipping the initial metadata rows
raw_data = pd.read_csv(file_path, header=None, skiprows=skip_rows)

# Define the column headers based on inspection
columns = [
    'Item Number', 'Item Name', 'Office #', 'UPC Code', 'On Hand', 
    'Wholesale Cost 1', 'Total Wholesale Cost 2', 'Your Cost 3', 
    'Total Your Cost 4', 'Retail Price 5', 'Total Retail Price 6',
]

# Drop unwanted columns (indices based on observation of your data)
raw_data = raw_data.drop(columns=[0, 1, 3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 17, 20, 22, 23, 25, 27, 29, 30, 32, 33])

# Assign the columns names to the DataFrame
raw_data.columns = columns

# Drop any rows where the 'Item Number' is NaN or contains 'Total' which are summary rows
raw_data = raw_data.dropna(subset=['Item Number'])
raw_data = raw_data[~raw_data['Item Number'].astype(str).str.contains('Total', na=False)]

# Further cleaning if needed (e.g., removing empty rows)
raw_data = raw_data.dropna(how='all')

pd.set_option('display.max_columns', 15)
# Reset the index
raw_data.reset_index(drop=True, inplace=True)

# clean data that has the $ symbol
cols_to_clean = ['Wholesale Cost 1', 'Total Wholesale Cost 2', 'Your Cost 3', 'Total Your Cost 4', 'Retail Price 5', 'Total Retail Price 6']

for col in cols_to_clean:
    raw_data[col] = raw_data[col].str.replace('$', '').astype(float)
    
# Display sorted values by column name
# raw_data.sort_values('Item Name').head(10)

# Use describe method to see some basic stats
# raw_data.describe()

# count number of unique values in each column
# raw_data.nunique()

######
# Question 1: Which frame has the biggest profit (Total Retail Price - Total Wholesale Cost)
######
raw_data['Profit'] = raw_data['Total Retail Price 6'] - raw_data['Total Wholesale Cost 2']

max_profit_frame = raw_data.loc[raw_data['Profit'].idxmax()]

print(max_profit_frame[['Item Number', 'Item Name', 'Total Wholesale Cost 2', 'Total Retail Price 6', 'Profit']])

######
# Question 2: The owners are moving their business to the UK and need their frames prices updated to the Pound currency
######
exchange_rate = 0.75  # 1 USD = 0.75 GBP

# Columns to convert
price_columns = ['Wholesale Cost 1', 'Total Wholesale Cost 2', 'Your Cost 3', 
                 'Total Your Cost 4', 'Retail Price 5', 'Total Retail Price 6']

# Function to convert USD to GBP
def convert_to_gbp(usd_value, rate):
    return round(usd_value * rate, 2)

# Apply the conversion
for col in price_columns:
    raw_data[col + ' (GBP)'] = raw_data[col].apply(lambda x: convert_to_gbp(x, exchange_rate))

# Save the updated DataFrame to a new CSV file
new_file_path = 'EV1_Frame_inventory_GBP.csv'
raw_data.to_csv(new_file_path, index=False)


# In[ ]:





# In[ ]:




