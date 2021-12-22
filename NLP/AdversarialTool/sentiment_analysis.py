"""
Define the prediction methods to be used when displaying the outputs on the webpage
"""
from transformers import pipeline, AutoTokenizer, AutoModel, DistilBertTokenizerFast, logging
import os
import torch

logging.set_verbosity_error()

def predictSentiment(text):
    sentiment_analysis = pipeline("sentiment-analysis")
    return sentiment_analysis(text)[0]


def predictStress(text):
    path="../saveModel"
    classifier=pipeline("sentiment-analysis", model=path)

    return classifier(text)[0]

def predictEmotions(text):
    classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True)
    prediction = classifier(text, )
    maxLabel=""
    maxScore=0
    for item in prediction[0]:
        if float(item["score"])>maxScore:
            maxScore=float(item["score"])
            maxLabel=item["label"]
    return maxLabel, maxScore, prediction
