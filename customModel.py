"""
This is the file that creates and saves the fine-tuned Distilbert model on the 'dreaddit-train.csv' dataset.
Run this file as is to recreate the model. The model will be made in the 'saveModel' directory.
More information about the model can be found in the description.txt file in the saveModel directory.
"""

import csv 
from transformers import DistilBertTokenizerFast, BertTokenizer, AdamW, DistilBertForSequenceClassification
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoModel
from torch.utils.data import DataLoader
import torch
from datasets import load_metric
from sklearn.model_selection import KFold
import pandas as pd
import os


os.makedirs("saveModel")

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')


def load_test_data():
    file = open("dreaddit-test.csv")
    csvreader = csv.reader(file)
    texts = []
    labels=[]
    for row in csvreader:
        texts.append(row[4])
        labels.append(row[5])
    file.close()
    return texts, labels

def load_training_data():
    file = open("dreaddit-train.csv")
    csvreader = csv.reader(file)
    next(csvreader)
    texts = []
    labels=[]
    for row in csvreader:
        texts.append(row[3])
        labels.append(int(row[5]))
    file.close()

    return texts, labels

print("loading training data")

train_texts, train_labels=load_training_data()
test_texts, test_labels=load_test_data()


train_encodings = tokenizer(train_texts, truncation=True, padding=True)
test_encodings = tokenizer(test_texts, truncation=True, padding=True)

print("data loaded and encoded")


class stressDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


train_dataset = stressDataset(train_encodings, train_labels)
test_dataset = stressDataset(test_encodings, test_labels)

print("data is a torch utils data dataset")

training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=5,              # total number of training epochs
    per_device_train_batch_size=16,  # batch size per device during training
    per_device_eval_batch_size=64,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
)

model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

trainer = Trainer(
    model=model,                         # the instantiated 🤗 Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=test_dataset             # evaluation dataset
)

print(trainer.train())
model.save_pretrained("saveModel")
tokenizer.save_pretrained("saveModel")



