import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset

# pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)  # 3 labels: positive, neutral, negative

review = pd.read_csv("olist_order_reviews_dataset.csv")

ratings = review["review_score"]

labels = []
for rating in ratings:
    if rating in [4, 5]:
        labels.append(0)  # positive
    elif rating == 3:
        labels.append(1)  # neutral
    elif rating in [1, 2]:
        labels.append(2)  # negative


texts = ["Rating: " + str(rating) for rating in ratings]

input_ids = []
attention_masks = []

for text in texts:
    encoded_dict = tokenizer(text, add_special_tokens=True, max_length=64, padding=True, 
                             return_attention_mask=True, return_tensors="pt")
    input_ids.append(encoded_dict["input_ids"])
    attention_masks.append(encoded_dict["attention_mask"])

input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)
labels = torch.tensor(labels)

dataset = TensorDataset(input_ids, attention_masks, labels)
train_loader = DataLoader(dataset, batch_size=32)

