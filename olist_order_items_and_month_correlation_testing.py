import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

order_item = pd.read_csv("olist_order_items_dataset.csv")


order_item['sales'] = order_item['price']

# convert 'shipping_limit_date' to datetime
order_item['shipping_limit_date'] = pd.to_datetime(order_item['shipping_limit_date'])

# extract the year and month 
order_item['order_year'] = order_item['shipping_limit_date'].dt.year
order_item['order_month'] = order_item['shipping_limit_date'].dt.month

# count the total sales for each year and month
yearly_order_counts = order_item.groupby('order_year')['order_item_id'].count()
print(yearly_order_counts)

filtered_data = order_item[(order_item['order_year'] == 2017) ]

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
ax.set_ylabel('Total Sales')
ax.set_title('Monthly Total Sales for 2017 in Olist')

# set x-axis months
ax.legend()
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.show()

# display summary table
# group by year and month and calculate the sum of sales
monthly_sales_summary = order_item.groupby(['order_year', 'order_month'])['sales'].sum().reset_index()

pivot_table = monthly_sales_summary.pivot(index='order_month', columns='order_year', values='sales')

# fill null with 0 
pivot_table = pivot_table.fillna(0)

# Calculate the correlation between sales and the month
correlation = pivot_table.corr().iloc[0, 1]
print("Correlation between sales and the month:", correlation)

print(pivot_table)
