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
    'Viper': OpenAttack.attackers.VIPERAttacker(),
    }


def getAttackOutput(text, label, attack):
    dataToAttack= datasets.Dataset.from_dict({
    "x": [
        text
    ],
    "y": [
        label
    ]
})
    attacker = AttackDict[attack]

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



