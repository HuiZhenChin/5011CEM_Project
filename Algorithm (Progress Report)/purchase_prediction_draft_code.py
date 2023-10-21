import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

order_item = pd.read_csv("olist_order_items_dataset.csv")
product = pd.read_csv("olist_products_dataset.csv")

product.dropna(inplace=True)

merge_data = pd.merge(order_item, product, on='product_id', how='inner')

merge_data['shipping_limit_date'] = pd.to_datetime(merge_data['shipping_limit_date'])

# extract the year
merge_data['order_year'] = merge_data['shipping_limit_date'].dt.year

# set the predicted year
merge_data['repurchased_next_year'] = 0
condition = (merge_data['order_year'] == 2018)
merge_data.loc[condition, 'repurchased_next_year'] = 1

# get the product category
unique_categories = merge_data['product_category_name'].unique()

for category in unique_categories:
    category_data = merge_data[merge_data['product_category_name'] == category]

    X = category_data.drop(["repurchased_next_year"], axis=1)  
    y = category_data["repurchased_next_year"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # select only numeric columns for X_train and X_test
    numeric_columns = X.select_dtypes(include=['number']).columns
    X_train = X_train[numeric_columns]
    X_test = X_test[numeric_columns]

    # implement the Random Forest classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # make predictions 
    y_pred = clf.predict(X_test)

    # print the accuracy for all categories
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Category: {category}")
    print("Accuracy:", accuracy)
    
    # predictions
    purchased_category = category if 1 in y_pred else "None"
    print(f"Predicted Purchased Category for {category}: {purchased_category}")

    # classification report 
    report = classification_report(y_test, y_pred)
    print(report)

