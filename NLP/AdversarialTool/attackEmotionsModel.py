import OpenAttack
import transformers
from transformers import AutoTokenizer, AutoModel, DistilBertTokenizerFast, DistilBertTokenizer, pipeline, AutoModelForSequenceClassification
from torch.utils.data import DataLoader
import torch
import datasets
from datasets import load_metric
import csv
from datasets import load_dataset

AttackDict={
    "Choose an attack: ":OpenAttack.attackers.BERTAttacker(),
    'BERT-ATTACK':OpenAttack.attackers.BERTAttacker(),
    'PWWS':OpenAttack.attackers.PWWSAttacker(),
    'Genetic':OpenAttack.attackers.GeneticAttacker(),
    'SememePSO':OpenAttack.attackers.PSOAttacker(),
    'FD': OpenAttack.attackers.FDAttacker(),
    'Viper': OpenAttack.attackers.VIPERAttacker()
    }

def getEmotionAttackOutput(text, attack):
    dataToAttack= datasets.Dataset.from_dict({
    "x": [
        text
    ]
    })
    attacker = AttackDict[attack]

    attack_eval = OpenAttack.AttackEval(attacker, victim, metrics = [
    OpenAttack.metric.EditDistance(),
    OpenAttack.metric.ModificationRate()
])

    print(attack_eval)
    eval = attack_eval.ieval(dataToAttack)
    return next(eval)

tokenizer = AutoTokenizer.from_pretrained('bhadresh-savani/distilbert-base-uncased-emotion')
model = AutoModelForSequenceClassification.from_pretrained('bhadresh-savani/distilbert-base-uncased-emotion')
victim = OpenAttack.classifiers.TransformersClassifier (model, tokenizer,  model.distilbert.embeddings.word_embeddings)

