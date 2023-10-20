import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

product= pd.read_csv("olist_products_dataset.csv")

# select top 20
top_categories = product['product_category_name'].value_counts().nlargest(20)

# bar plot 
plt.figure(figsize=(12, 6))
sns.barplot(x=top_categories.values, y=top_categories.index, orient='h')
plt.title('Top 20 Product Categories by Count in Olist')
plt.xlabel('Product Item Count')
plt.ylabel('Product Category')
plt.show()


