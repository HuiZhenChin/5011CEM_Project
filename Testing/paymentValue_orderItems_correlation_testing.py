# Order items and payment values correlation test

import pandas as pd
from scipy.stats import pearsonr

# Load the datasets
order_items = pd.read_csv("olist_order_items_dataset.csv")
order_payments = pd.read_csv("olist_order_payments_dataset.csv")

# Convert 'order_item_id' to integer
order_items['order_item_id'] = order_items['order_item_id'].astype(int)

# Merge the relevant columns on 'order_id' to combine order items and payment data
merged_data = order_items[['order_id', 'order_item_id']].merge(order_payments[['order_id', 'payment_value']], 
                                                               on='order_id', how='inner')

# Calculate the Pearson correlation coefficient and p-value
correlation_coefficient, p_value = pearsonr(merged_data['order_item_id'], merged_data['payment_value'])

print("Correlation between number of order items and payment values:", correlation_coefficient)
print("P-value:", p_value)


