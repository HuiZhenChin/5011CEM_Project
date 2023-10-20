import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

order_items = pd.read_csv("olist_order_items_dataset.csv")

# group 'order_id' to calculate the total price and number of items purchased
order_totals = order_items.groupby('order_id').agg({'price': 'sum', 'order_item_id': 'count'}).reset_index()
order_totals.columns = ['order_id', 'total_price', 'num_items']

# box plot 
plt.figure(figsize=(10, 6))
sns.boxplot(x='num_items', y='total_price', data=order_totals, color='skyblue')
plt.title('Total Price vs. Number of Items Purchased')
plt.xlabel('Number of Items Purchased')
plt.ylabel('Total Price')

plt.show()

pivot_table = pd.pivot_table(order_totals, index='num_items', values='total_price', aggfunc='sum')

# pivot table
print(pivot_table)
