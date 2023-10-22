import pandas as pd
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

review = pd.read_csv("olist_order_reviews_dataset.csv")

review['review_answer_timestamp'] = pd.to_datetime(review['review_answer_timestamp'])

# create two time boundaries 
morning_boundary = 12  # 12 pm to 5.59 pm
evening_boundary = 18  # 6 pm to 11.59 am

morning_group = review[review['review_answer_timestamp'].dt.hour < morning_boundary]['review_score']
evening_group = review[review['review_answer_timestamp'].dt.hour >= evening_boundary]['review_score']

#pPerform two-sample t-test
t_statistic, p_value = ttest_ind(morning_group, evening_group, equal_var=False)  # Assuming unequal variances


# significance level (alpha)
alpha = 0.05


print("T-statistic:", t_statistic)
print("P-value:", p_value)

# compare the p-value to the alpha level
if p_value < alpha:
    print("Reject the null hypothesis: There is a statistically significant difference in review scores between morning and evening reviews.")
else:
    print("Fail to reject the null hypothesis: There is no statistically significant difference in review scores between morning and evening reviews.")

# plot the density graph
plt.figure(figsize=(8, 6))
sns.kdeplot(morning_group, label='Morning', shade=True, color='blue')
sns.kdeplot(evening_group, label='Evening', shade=True, color='orange')
plt.title('Review Score Distribution by Time of Day')
plt.xlabel('Review Score')
plt.ylabel('Density')
plt.legend()
plt.show()

