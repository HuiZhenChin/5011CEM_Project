import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

order_item = pd.read_csv("olist_order_items_dataset.csv")
payment = pd.read_csv("olist_order_payments_dataset.csv")
order = pd.read_csv("olist_orders_dataset.csv")

merge_data = pd.merge(order, order_item, on='order_id', how='inner')
merge_data = pd.merge(merge_data, payment, on='order_id', how='inner')

merge_data['order_purchase_timestamp'] = pd.to_datetime(merge_data['order_purchase_timestamp'])

# extract the year 
merge_data['order_year'] = merge_data['order_purchase_timestamp'].dt.year
merge_data['order_month'] = merge_data['order_purchase_timestamp'].dt.month

# get data of 2017
merge_data_2017 = merge_data[(merge_data['order_year'] == 2017)]

# extract 'order_item_id' and 'order_month' columns
X = merge_data_2017[['order_item_id', 'order_month']]

# feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# initialize KMeans model with K clusters 
kmeans = KMeans(n_clusters=3, random_state=42, init='k-means++', n_init=10, max_iter=300)

# fit the model
kmeans.fit(X_scaled)

# cluster label
cluster_labels = kmeans.labels_

# declare centroids
centroids = kmeans.cluster_centers_

# K-Means Loop
while True:
    # calculate distances from data points to centroids
    distances = np.linalg.norm(X_scaled[:, np.newaxis, :] - centroids, axis=2)

    # assign data points to its nearest centroid
    new_labels = np.argmin(distances, axis=1)

    # check if any data point has changed its cluster
    if not np.array_equal(new_labels, cluster_labels):
        cluster_labels = new_labels
    else:
        break

    # update centroids based on new cluster 
    for i in range(3):
        centroids[i] = X_scaled[cluster_labels == i].mean(axis=0)

# visualize the clusters
plt.figure(figsize=(10, 6))
for cluster_id in range(3):
    cluster_data = X[cluster_labels == cluster_id]
    plt.scatter(cluster_data['order_month'], cluster_data['order_item_id'], label=f'Cluster {cluster_id}')

# plot centroids
plt.scatter(centroids[:, 1], centroids[:, 0], marker='x', s=100, c='black', label='Centroids')

# plot the x and y axis
plt.title('K-Means Clustering of Order Items by Month')
plt.xlabel('Order Month')
plt.ylabel('Order Item')
plt.legend()

plt.show()

# pivot table of the order item count for each month
pivot_table = merge_data_2017.pivot_table(index='order_month', values='order_item_id', aggfunc='count')

pivot_table = pivot_table.rename(columns={'order_item_id': 'order_item_count'})

print(pivot_table)

