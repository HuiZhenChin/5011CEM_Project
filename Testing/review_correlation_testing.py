# correlation testing

import pandas as pd
from scipy.stats import pearsonr

review= pd.read_csv("olist_order_reviews_dataset.csv")
product= pd.read_csv("olist_products_dataset.csv")
order_item = pd.read_csv("olist_order_items_dataset.csv")

review['review_comment_title'].fillna("No Title", inplace=True)
review['review_comment_message'].fillna("No Message", inplace=True)


merge_data = review.merge(order_item, on='order_id', how='inner')

# calculate the correlation coefficient between 'price' and 'review_score'
correlation_coefficient, p_value = pearsonr(merge_data['price'], merge_data['review_score'])

print("Pearson Correlation Coefficient:", correlation_coefficient)
print("P-value:", p_value)

