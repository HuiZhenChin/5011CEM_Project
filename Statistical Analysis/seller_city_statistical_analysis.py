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

geolocation= pd.read_csv("olist_geolocation_dataset.csv")
seller= pd.read_csv("olist_sellers_dataset.csv")

    
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

seller_count = seller.groupby('seller_city')['seller_id'].count().reset_index()
seller_count.rename(columns={'seller_id': 'seller_count'}, inplace=True)

# calculate the customer count for each state
seller_count = seller['seller_city'].value_counts().reset_index()
seller_count.columns = ['seller_city', 'seller_count']

# merge the 'customer_count' data with 'gdf' based on the 'customer_state' column
gdf = gdf.merge(seller_count, left_on='ADM2_PT', right_on='seller_city', how='left')


# plot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
gdf.boundary.plot(ax=ax, linewidth=1, color='k')  # Plot boundaries

# color the map with different colour tone to indicate the count
gdf.plot(column='seller_count', ax=ax, legend=True, cmap=cmap, legend_kwds={'label': "Seller Count", 'orientation': "vertical", 'shrink': 0.5})

legend = ax.get_legend()

# plot title
plt.title("Seller Distribution in Brazil City")

# show the plot
plt.show()

# summarise the total count for eeach city
print("Seller Count for Each City:")
print(seller_count)