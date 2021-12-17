from django.shortcuts import render
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
    ("Choose an attack: ","Choose an attack: " ),
    ('BERT-ATTACK', 'BERT-ATTACK(Default)'),
    ('PWWS','PWWS'),
    ('Genetic', 'Genetic'),
    ('SememePSO', 'SememePSO'),
    ('FD', 'FD'),
    ('Viper', 'Viper')
    ]

class NewForm(forms.Form):
    inputText = forms.CharField(widget=forms.Textarea, label='')
    chosenAttack= forms.CharField(label=mark_safe('<br />'), widget=forms.Select(choices=ATTACK_CHOICES))



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

        return render(request, "AdversarialTool/index.html", {
        "form":NewForm(request.POST), "textInputted":textInputted, "givenText":attackOutputResults, "startingClassification":classifier,
        "attackedClassification":attackOutputClasification, "attackSucess":attackSucess, "origText": givenText, "attackType":attackType
    })
    else:
        return render(request, "AdversarialTool/index.html", {
            "form":NewForm(), "textInputted":False, "givenText":""
        })

def emotions(request):
    if request.method == "POST":
        render(request, "AdversarialTool/loading.html")
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
        return render(request, "AdversarialTool/emotions.html", {
        "form":NewForm(request.POST), "givenText":givenText, "startingClassification":classifier[0], "textInputted":textInputted, "attackSucess":attackSucess
        ,"OutputResults":attackOutputResults, "attackedClassification":attackOutputClasification, "attackType":attackType
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

def loading(request):
    return render(request, "AdversarialTool/loading.html")

def login_view(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        if request.POST.get("Login"):
            user=authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return render(request, "AdversarialTool/index.html", {
                "form":NewForm(), "textInputted":False, "givenText":""
            })
        elif request.POST.get("Sign Up"):
            User.objects.create_user(username, "",password)
            user=authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return render(request, "AdversarialTool/index.html", {
                "form":NewForm(), "textInputted":False, "givenText":""
            })
        else:
            return render(request, "AdversarialTool/login.html",{'message':"Invalid Login Information: Either sign up or review your login information"})
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
