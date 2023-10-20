# number of customer count in each Brazil city

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import geopandas as gpd
import shapefile as shp
import seaborn as sns 
import warnings 
import unidecode
import re
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

    
# plot layout
sns.set(style="whitegrid", palette="pastel", color_codes=True)
# get the sharpfile (map file)
shp_path = "D:/INTI Degree/DEG YEAR 2 INTI-Sem 5/Big Data Programming Project/Brazil/bra_admbnda_adm2_ibge_2020.shp"
gdf = gpd.read_file(shp_path)

# define the number of bins and colormap 
bins = 5  
cmap = 'rainbow'  # colour tone

# customer city: remove the symbol and convert to lower case
gdf['ADM2_PT'] = gdf['ADM2_PT'].apply(lambda x: unidecode.unidecode(x))
gdf['ADM2_PT'] = gdf['ADM2_PT'].str.replace('[^\w\s]', ' ', regex=True)
gdf['ADM2_PT'] = gdf['ADM2_PT'].str.lower()

def clean_city_name(city_name):
    # Remove symbols, diacritics, and convert to lowercase
    cleaned_name = re.sub(r'[^A-Za-z0-9\s]', '', city_name).lower()
    return cleaned_name

geolocation['geolocation_city'] = geolocation['geolocation_city'].apply(clean_city_name)

# merge 'customer_count' data with 'gdf' based on the 'full_state_name' column
customer_count = customer.groupby('customer_city')['customer_id'].count().reset_index()
customer_count.rename(columns={'customer_id': 'customer_count'}, inplace=True)

# calculate the customer count for each state
customer_count = customer['customer_city'].value_counts().reset_index()
customer_count.columns = ['customer_city', 'customer_count']

# merge the 'customer_count' data with 'gdf' based on the 'customer_state' column
gdf = gdf.merge(customer_count, left_on='ADM2_PT', right_on='customer_city', how='left')


# Pplot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
gdf.boundary.plot(ax=ax, linewidth=1, color='k')  # Plot boundaries

# color the map with different colour tone to indicate the count
gdf.plot(column='customer_count', ax=ax, legend=True, cmap=cmap, legend_kwds={'label': "Customer Count", 'orientation': "vertical", 'shrink': 0.5})

legend = ax.get_legend()

# plot title
plt.title("Customer Distribution in Brazil City")

# show the plot
plt.show()

# summarise the total count for eeach city
print("Customer Count for Each City:")
print(customer_count)

