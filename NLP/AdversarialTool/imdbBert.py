from datasets import load_dataset
from sklearn.model_selection import train_test_split
from pathlib import Path
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, AutoModelForSequenceClassification, TrainingArguments
import tensorflow as tf
from transformers import Trainer

import numpy as np
from datasets import load_metric

raw_datasets = load_dataset("imdb")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)

small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))
full_train_dataset = tokenized_datasets["train"]
full_eval_dataset = tokenized_datasets["test"]

print("done loading and tokenizing the data")

def keras():
    model = TFAutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)

    tf_train_dataset = small_train_dataset.remove_columns(["text"]).with_format("tensorflow")
    tf_eval_dataset = small_eval_dataset.remove_columns(["text"]).with_format("tensorflow")

    train_features = {x: tf_train_dataset[x] for x in tokenizer.model_input_names}
    train_tf_dataset = tf.data.Dataset.from_tensor_slices((train_features, tf_train_dataset["label"]))
    train_tf_dataset = train_tf_dataset.shuffle(len(tf_train_dataset)).batch(8)

    eval_features = {x: tf_eval_dataset[x] for x in tokenizer.model_input_names}
    eval_tf_dataset = tf.data.Dataset.from_tensor_slices((eval_features, tf_eval_dataset["label"]))
    eval_tf_dataset = eval_tf_dataset.batch(8)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=tf.metrics.SparseCategoricalAccuracy(),
    )

    model.fit(train_tf_dataset, validation_data=eval_tf_dataset, epochs=3)


model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=2)

training_args = TrainingArguments("test_trainer")


trainer = Trainer(
    model=model, args=training_args, train_dataset=small_train_dataset, eval_dataset=small_eval_dataset
)

trainer.train()

metric = load_metric("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


trainer.evaluate()