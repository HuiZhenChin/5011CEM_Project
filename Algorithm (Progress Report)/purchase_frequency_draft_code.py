import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# Load your data and preprocess it if needed
order_item = pd.read_csv("olist_order_items_dataset.csv")
payment = pd.read_csv("olist_order_payments_dataset.csv")
order = pd.read_csv("olist_orders_dataset.csv")

# Merge data from different sources
merge_data = pd.merge(order, order_item, on='order_id', how='inner')
merge_data = pd.merge(merge_data, payment, on='order_id', how='inner')

# Extract the year and month from the order purchase timestamp
merge_data['order_purchase_timestamp'] = pd.to_datetime(merge_data['order_purchase_timestamp'])
merge_data['order_month'] = merge_data['order_purchase_timestamp'].dt.month
merge_data['order_year'] = merge_data['order_purchase_timestamp'].dt.year

# Filter data for the year 2017
merge_data_2017 = merge_data[(merge_data['order_year'] == 2017) & (merge_data['payment_type'] != 'not_defined')]

# Extract the 'order_item_id' and 'payment_value' columns
data = merge_data_2017[['order_item_id', 'payment_value']].to_numpy()

# Number of clusters (K)
num_clusters = 3

# Initialize the KMeans model with 'k-means++' initialization and a larger 'n_init' value
kmeans = KMeans(n_clusters=num_clusters, random_state=42, init='k-means++', n_init=100, max_iter=300)

# Fit the model to the data
kmeans.fit(data)

# Get cluster labels and centroids
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

# Visualize the clustering results
plt.figure(figsize=(10, 6))
for cluster_id in range(num_clusters):
    cluster_data = data[labels == cluster_id]
    plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {cluster_id}')

# Plot centroids
plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=100, c='black', label='Centroids')

# Add labels and a legend to the plot
plt.xlabel('Order Item')
plt.ylabel('Payment Value')
plt.legend()

# Show the scatter plot
plt.show()



# Create a pivot table to show the order item count for each month
pivot_table = merge_data_2017.pivot_table(index='order_month', values='order_item_id', aggfunc='count')

# Rename the columns for clarity
pivot_table = pivot_table.rename(columns={'order_item_id': 'order_item_count'})

# Display the pivot table
print(pivot_table)
