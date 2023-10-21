import pandas as pd 
import numpy as np 
import seaborn as sns 
import warnings 

warnings.filterwarnings('ignore')

seller= pd.read_csv("C:/Users/JQgam/Downloads/olist_sellers_dataset.csv")


print ("Seller")
seller.head()
seller.info()

print ("Unique: ")
seller.nunique()

print ("Unique: ")
list_a = []
for s in seller['seller_city'].unique():
   list_a.append(s)
print(list_a)
print(list_a.__len__())

print("Null Value: ")
seller.isnull().sum()

print("Null Value Percentage: ")
(seller.isnull().sum()/(len(seller)))*100