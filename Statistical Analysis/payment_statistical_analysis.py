import pandas as pd 
import numpy as np 
import seaborn as sns 
import warnings 
import matplotlib.pyplot as plt 
warnings.filterwarnings('ignore')

payment= pd.read_csv("olist_order_payments_dataset.csv")

payment['payment_value'] = payment['payment_value'].round(2)

payment = payment[payment['payment_type'] != 'not_defined']

payment.reset_index(drop=True, inplace=True)

# Ggoup the data by 'payment_type' and calculate the average 'payment_value' 
average_payment_by_method = payment.groupby('payment_type')['payment_value'].mean()

average_payment_by_method = average_payment_by_method.reset_index()

# rename the columns 
average_payment_by_method.columns = ['Payment Method', 'Average Payment Value']

print(average_payment_by_method)

plt.figure(figsize=(10, 6))
sns.barplot(x='Average Payment Value', y='Payment Method', data=average_payment_by_method, palette="pastel")
plt.title('Average Payment Value by Payment Method in Olist')
plt.xlabel('Average Payment Value')
plt.ylabel('Payment Method')

plt.show()
