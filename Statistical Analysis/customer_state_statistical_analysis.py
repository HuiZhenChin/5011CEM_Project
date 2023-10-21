# number of customer count in each Brazil state

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import geopandas as gpd
import shapefile as shp
import seaborn as sns 
import warnings 
warnings.filterwarnings('ignore')

customer= pd.read_csv("olist_customers_dataset.csv")
geolocation= pd.read_csv("olist_geolocation_dataset.csv")
order_item= pd.read_csv("olist_order_items_dataset.csv")
payment= pd.read_csv("olist_order_payments_dataset.csv")
review= pd.read_csv("olist_order_reviews_dataset.csv")
order= pd.read_csv("olist_orders_dataset.csv")
product= pd.read_csv("olist_products_dataset.csv")
seller= pd.read_csv("olist_sellers_dataset.csv")
product_category= pd.read_csv("product_category_name_translation.csv")


# view how many state in dataset
unique_states = customer['customer_state'].unique()

print("Unique States in the Dataset:")
for state in unique_states:
   print(state)
    
# plot layout    
sns.set(style="whitegrid", palette="pastel", color_codes=True)
shp_path = "D:/INTI Degree/DEG YEAR 2 INTI-Sem 5/Big Data Programming Project/Brazil/bra_admbnda_adm2_ibge_2020.shp"
gdf = gpd.read_file(shp_path)

# number of bins 
bins = 5  
cmap = 'gist_earth'  

# state short form to its full name
state_mapping = {
    'SP': 'São Paulo',
    'SC': 'Santa Catarina',
    'MG': 'Minas Gerais',
    'PR': 'Paraná',
    'RJ': 'Rio de Janeiro',
    'RS': 'Rio Grande do Sul',
    'PA': 'Pará',
    'GO': 'Goiás',
    'ES': 'Espírito Santo',
    'BA': 'Bahia',
    'MA': 'Maranhão',
    'MS': 'Mato Grosso',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'RN': 'Rio Grande do Norte',
    'PE': 'Pernambuco',
    'MT': 'Mato Grosso',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'AL': 'Alagoas',
    'RO': 'Rondônia',
    'PB':' Paraíba',
    'TO': 'Tocantins',
    'PI': 'Piauí',
    'AC': 'Acre',
    'SE': 'Sergipe',
    'RR': 'Roraima'
   
}

# create a new column with full state names in the customer dataset
customer['full_state_name'] = customer['customer_state'].map(state_mapping)

# merge 'customer_count' data with 'gdf' based on the 'full_state_name' column
customer_count = customer.groupby('full_state_name')['customer_id'].count().reset_index()
customer_count.rename(columns={'customer_id': 'customer_count'}, inplace=True)

# accumulate the customer count for each state
customer_count = customer['full_state_name'].value_counts().reset_index()
customer_count.columns = ['customer_state', 'customer_count']

# merge the 'customer_count' data with 'gdf' based on the 'customer_state' 
gdf = gdf.merge(customer_count, left_on='ADM1_PT', right_on='customer_state', how='left')


# plot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
gdf.boundary.plot(ax=ax, linewidth=1, color='k')  

# use the 'customer_count' column to define the color tone
gdf.plot(column='customer_count', ax=ax, legend=True, cmap=cmap, legend_kwds={'label': "Customer Count", 'orientation': "vertical", 'shrink': 0.5})

legend = ax.get_legend()

plt.title("Customer Distribution in Brazil State")

plt.show()

# summarise the total count for eeach city
print("Customer Count for Each State:")
print(customer_count)
