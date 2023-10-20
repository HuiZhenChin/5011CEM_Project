import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

order_item = pd.read_csv("olist_order_items_dataset.csv")

# convert 'shipping_limit_date' to datetime
order_item['shipping_limit_date'] = pd.to_datetime(order_item['shipping_limit_date'])

# extract the year and month 
order_item['order_year'] = order_item['shipping_limit_date'].dt.year
order_item['order_month'] = order_item['shipping_limit_date'].dt.month

# count the total order item for each year
yearly_order_counts = order_item.groupby('order_year')['order_item_id'].count()
print(yearly_order_counts)

# pick the comparable year which is 2017 and 2018
filtered_data = order_item[(order_item['order_year'] == 2017) | (order_item['order_year'] == 2018)]

# group the filtered data by year and month
monthly_order_counts = filtered_data.groupby(['order_year', 'order_month'])['order_item_id'].count().unstack()

# extract the year and month
years = monthly_order_counts.index
months = monthly_order_counts.columns


# create an array to represent the x-axis 
x = np.arange(len(months))

# create a line graph
fig, ax = plt.subplots(figsize=(10, 6))

# loop the years and plot line graph
for year in years:
    if year in monthly_order_counts.index:
        if year == 2017:
            color = 'orange'  # orange for 2017
        elif year == 2018:
            color = 'blue'    # blue for 2018
        ax.plot(months, monthly_order_counts.loc[year], label=year, color=color, marker='o')

# labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Order Item Count')
ax.set_title('Monthly Order Item Count for 2017 and 2018 in Olist')

# set x-axis months
ax.legend()
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.show()

# display summary table
# group by year and month and calculate the count
monthly_order_counts = filtered_data.groupby(['order_year', 'order_month']).size().reset_index(name='count')

pivot_table = monthly_order_counts.pivot(index='order_month', columns='order_year', values='count')

# fill null with 0 
pivot_table = pivot_table.fillna(0).astype(int)

print(pivot_table)
