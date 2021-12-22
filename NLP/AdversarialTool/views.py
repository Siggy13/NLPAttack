'''
File that takes care of all http requests and responses. Every HTML template is rendered through this file.
Makes the project useable through calling methods to add functionality.

'''
from django.shortcuts import render, redirect, reverse
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.conf import settings
from AdversarialTool.sentiment_analysis import predictSentiment , predictStress, predictEmotions
from AdversarialTool.attackFineTunedModel import getAttackOutput
from AdversarialTool.attackEmotionsModel import getEmotionAttackOutput
from django.utils.safestring import mark_safe
from django.forms import Textarea
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Attacks


ATTACK_CHOICES= [
    ("BERT-ATTACK","Choose an attack: " ),
    ('BERT-ATTACK', 'BERT-ATTACK(Default)'),
    ('PWWS','PWWS'),
    ('Genetic', 'Genetic'),
    ('SememePSO', 'SememePSO'),
    ('Viper', 'Viper'),
    ]

class NewForm(forms.Form):
    inputText = forms.CharField(widget=forms.Textarea, label='')
    chosenAttack= forms.CharField(label=mark_safe('<br />'), widget=forms.Select(choices=ATTACK_CHOICES))


'''Renders page that performs stress-based classification and adversarial attack'''
def index(request):
    
    if request.method == "POST":
        givenText = request.POST.get("inputText")
        attackType= request.POST.get("chosenAttack")

        textInputted=True
        classifier=predictStress(givenText)
        if classifier['label']=='LABEL_1':
            label=1
            classifier="Stressed"
        elif classifier['label']=='LABEL_0':
            classifier="Not Stressed"
            label=0

        attackOutput=getAttackOutput(givenText,label, attackType)

        attackOutputClasification=AttackClassification(attackOutput, label)
        attackSucess=isAttackSucessful(attackOutput)
        if attackSucess:
            attackOutputResults=attackOutput["result"]
        else:
            attackOutputResults=givenText
        bold = lambda x: f'<b>{x}</b>'
        parsedlist=highlight_shared(givenText, attackOutputResults, bold)
        return render(request, "AdversarialTool/index.html", {
        "form":NewForm(request.POST), "textInputted":textInputted, "givenText":attackOutputResults, "startingClassification":classifier,
        "attackedClassification":attackOutputClasification, "attackSucess":attackSucess, "origText": givenText, "attackType":attackType,
        "mylist":parsedlist
    })
    else:
        return render(request, "AdversarialTool/index.html", {
            "form":NewForm(), "textInputted":False, "givenText":""
        })

'''Renders page that performs emotion-based classification and adversarial attack'''
def emotions(request):
    if request.method == "POST":
        givenText = request.POST.get("inputText")
        attackType= request.POST.get("chosenAttack")

        textInputted=True
        classifier=predictEmotions(givenText)

        attackOutput=getEmotionAttackOutput(givenText,attackType)
        print(attackOutput)
        attackSucess=isAttackSucessful(attackOutput)
        if attackSucess:
            attackOutputResults=attackOutput["result"]
        else:
            attackOutputResults=givenText

        attackOutputClasification=predictEmotions(attackOutputResults)[0]
        bold = lambda x: f'<b>{x}</b>'
        parsedlist=highlight_shared(givenText, attackOutputResults, bold)
        return render(request, "AdversarialTool/emotions.html", {
        "form":NewForm(request.POST), "givenText":givenText, "startingClassification":classifier[0], "textInputted":textInputted, "attackSucess":attackSucess
        ,"OutputResults":attackOutputResults, "attackedClassification":attackOutputClasification, "attackType":attackType, "mylist":parsedlist
    })
    else:
        return render(request, "AdversarialTool/emotions.html", {
            "form":NewForm(), "textInputted":False, "givenText":""
        })
def FAQ(request):
    return render(request, "AdversarialTool/FAQ.html")

def examples(request):
    return render(request, "AdversarialTool/examples.html")

def about(request):
    return render(request, "AdversarialTool/about.html")

def aboutAttacks(request):
    return render(request, "AdversarialTool/aboutAttacks.html")

def delete_attack(request, attack_id):
    attack=Attacks.objects.get(pk=attack_id)
    attack.delete()
    return redirect('/AdversarialTool/savedAttacks')

def login_view(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        if username=="" or password=="":
            return render(request, "AdversarialTool/login.html",{'message':"Invalid Information: Please fill in both the username and password feilds"})
        if request.POST.get("Login"):
            user=authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return render(request, "AdversarialTool/index.html", {
                "form":NewForm(), "textInputted":False, "givenText":""
            })
            else:
                return render(request, "AdversarialTool/login.html",{'message':"Invalid Login Information: Please check your username and password"})
        elif request.POST.get("Sign Up"):
            if User.objects.filter(username=username).exists():
                return render(request, "AdversarialTool/login.html",{'message':"This username already exisits, please choose a new one."})
            User.objects.create_user(username, "",password)
            user=authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return render(request, "AdversarialTool/index.html", {
                "form":NewForm(), "textInputted":False, "givenText":""
            })

    return render(request, "AdversarialTool/login.html")


def logout_view(request):
    logout(request)
    return render(request, "AdversarialTool/login.html",{'message':"You have been logged out."})
    
def savedAttacks(request):
    if request.method=="POST":
        attackOutput=request.POST.get("attack")
        originalText=request.POST.get("origInput")
        user=request.user
        attackType=request.POST.get("attackType")
        originalClassification=request.POST.get("originalClassification")
        newClassification=request.POST.get("newClassification")

        attack=Attacks(originalText=originalText, AttackedText=attackOutput, User=user, attackType=attackType, 
        originalClassification=originalClassification, newClassification=newClassification)
        attack.save()

    userAttacks=Attacks.objects.filter(User=request.user).values()
    listOfAttacks=[]
    eachAttack=[]
    for dictionary in userAttacks:
        eachAttack.append(dictionary["originalText"])
        eachAttack.append(dictionary["originalClassification"])
        eachAttack.append(dictionary["attackType"])
        eachAttack.append(dictionary["AttackedText"])
        eachAttack.append(dictionary["newClassification"])
        eachAttack.append(dictionary["id"])
        listOfAttacks.append(eachAttack)
        eachAttack=[]
    return render(request, "AdversarialTool/savedAttacks.html", {"attacks":listOfAttacks})


def AttackClassification(attackDict, label):
    if attackDict["success"] and label==1:
        return "Not Stressed"
    elif attackDict["success"] and label==0:
        return "Stressed"
    elif not attackDict["success"] and label==1:
        return "Stressed"
    else:
        return "Not Stressed"
def isAttackSucessful(attackDict):
    if attackDict["success"]:
        return True
    else: 
        return False

def highlight_shared(string2, string1, format_func):
    shared_toks = set(string1.split(' ')) & set(string2.split(' '))
    return ' '.join([format_func(tok) if tok not in shared_toks else tok for tok in string1.split(' ') ])