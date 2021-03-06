"""
Builds the attack for the fine-tuned stress classification model
"""
import OpenAttack
import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DistilBertTokenizerFast
from torch.utils.data import DataLoader
import torch
import datasets
from datasets import load_metric
import csv



AttackDict={
    "Choose an attack: ":OpenAttack.attackers.BERTAttacker(),
    'BERT-ATTACK':OpenAttack.attackers.BERTAttacker(),
    'PWWS':OpenAttack.attackers.PWWSAttacker(),
    'Genetic':OpenAttack.attackers.GeneticAttacker(),
    'SememePSO':OpenAttack.attackers.PSOAttacker(),
    'Viper': OpenAttack.attackers.VIPERAttacker(method = 'dces'),
    }


def getAttackOutput(text, label, attack):
    """
    Returns the result of an attack using OpenAttack's ieval method
    """
    dataToAttack= datasets.Dataset.from_dict({
    "x": [
        text
    ],
    "y": [
        label
    ]
})
    attacker = AttackDict[attack]
    #Metrics available for testing--only the text output, classification, and success are displayed on the web page
    attack_eval = OpenAttack.AttackEval(attacker, victim, metrics = [
    OpenAttack.metric.EditDistance(),
    OpenAttack.metric.ModificationRate()
])
    eval = attack_eval.ieval(dataToAttack)
    return next(eval)

path="../saveModel"
tokenizer = transformers.AutoTokenizer.from_pretrained(path)
model = transformers.AutoModelForSequenceClassification.from_pretrained(path, num_labels=2, output_hidden_states=False)
victim = OpenAttack.classifiers.TransformersClassifier (model, tokenizer, model.distilbert.embeddings.word_embeddings)



