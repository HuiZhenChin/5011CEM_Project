import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

order_items = pd.read_csv("olist_order_items_dataset.csv")

# group 'seller_id' and calculate number of order items sold 
seller_order_items = order_items.groupby('seller_id')['order_item_id'].count().reset_index()
seller_order_items.columns = ['seller_id', 'num_order_items_sold']

# sort the sellers by the number of order items sold in descending order
sorted_sellers = seller_order_items.sort_values(by='num_order_items_sold', ascending=False)

# top 3 highest sold sellers
top_sellers = sorted_sellers.head(3)


remaining_sellers = sorted_sellers.iloc[3:]  # top 3 highest sales
random_sellers = remaining_sellers.sample(n=17) # 17 random selected

# top 3 and the 17 random selected sellers
sample_sellers = pd.concat([top_sellers, random_sellers])

# bar plot 
plt.figure(figsize=(10, 6))
sns.barplot(x='seller_id', y='num_order_items_sold', data=sample_sellers, palette='pastel')
plt.title('Sample of 10 Sellers')
plt.xlabel('Seller ID')
plt.ylabel('Number of Order Items Sold')
plt.xticks(rotation=45)  

plt.show()

