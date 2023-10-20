import pandas as pd 
import numpy as np 
import seaborn as sns 
import warnings 
warnings.filterwarnings('ignore')

payment= pd.read_csv("olist_order_payments_dataset.csv")

print ("Payments")
payment.info()

print ("Unique: ")
for p in payment['payment_value'].unique():
   print(p)

print("Null Value: ")
payment.isnull().sum()

print("Null Value Percentage: ")
(payment.isnull().sum()/(len(payment)))*100

payment['payment_value'] = payment['payment_value'].round(2)

print(payment.head())