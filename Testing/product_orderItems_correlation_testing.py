# Product sales and order items correlation test

import pandas as pd
from scipy.stats import pearsonr

order_items = pd.read_csv("olist_order_items_dataset.csv")
order_payments = pd.read_csv("olist_order_payments_dataset.csv")

# Merge the relevant columns on 'order_id' to combine order items and payment data
merged_data = order_items[['order_id', 'order_item_id', 'price']].merge(order_payments[['order_id', 'payment_value']], 
                                                                        on='order_id', how='inner')

# Calculate correlation coefficient between order_item_id and price
correlation_coefficient_product_sales, p_value_product_sales = pearsonr(merged_data['order_item_id'], merged_data['price'])

print("Pearson Correlation Coefficient between number of order items and product sales:", correlation_coefficient_product_sales)
print("P-value:", p_value_product_sales)








# Calculate the correlation between order_item_id and both price and payment_value
#correlation_order_items_sales = merged_data['order_item_id'].corr(merged_data['price'])
#correlation_order_items_payments = merged_data['order_item_id'].corr(merged_data['payment_value'])

#print("Correlation between number of order items and product sales:", correlation_order_items_sales)
#print("Correlation between number of order items and payment values:", correlation_order_items_payments)