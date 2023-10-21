# Customer and geolocation correlation test

import pandas as pd
from scipy.stats import pearsonr

# Load the datasets
customers = pd.read_csv("olist_customers_dataset.csv")
geolocation = pd.read_csv("olist_geolocation_dataset.csv")

# Merge the necessary data for zip code correlation
geo_correlation = customers.merge(geolocation, left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix", 
                                      how="inner")

# Calculate the Pearson correlation coefficient and p-value
correlation_coefficient = pearsonr(geo_correlation["customer_zip_code_prefix"], 
                                       geo_correlation["geolocation_zip_code_prefix"])

print("Pearson Correlation Coefficient between customer zip codes and geolocation zip codes:", correlation_coefficient[0])
print("P-value:", correlation_coefficient[1])
