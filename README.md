# MisclassifyMe: 
This project is an implementation of an adversarial attack on natural language processing models.

## The Purpose of the Project:
The usage of machine learning to monitor student online activity is a rapidly growing industry. 
While there is increasing scrutiny of the companies that sell school machine learning services, there is limited technical examination
of the algorithms themselves because of the companies’ lack of transparency. The field of adversarial machine learning on natural 
 language processing (NLP) models is becoming a useful way to discover vulnerabilities in these models. MisclassifyMe develops a tool 
 that uses an adversarial model to transform input text into an output that can mislead an NLP algorithm fine-tuned towards detecting 
 mental health issues in order to approximate the kinds of models being used in schools. We use two fine-tuned implementations of 
 BERT as our classifiers and then employ a variety of adversarial attacks from the <a href='https://openattack.readthedocs.io/en/latest/apis/attacker.html'
 style="padding:0">OpenAttack API</a> to generate altered outputs. The stress
 related model is a DistilBERT model from the <a href="https://huggingface.co/docs/transformers/model_doc/distilbert" style="padding:0">
Transformers library</a> fine-tuned on a <a href="https://arxiv.org/pdf/1911.00133.pdf" style="padding:0">dataset</a> that 
classifies the how stressed a piece of text sounds. The second model is a 
<a href=https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion style="padding:0">pretrained
 DistilBERT model</a> from the Transformers library that classifies what emotion a piece of text emenates.
 
 ## How to Install the Project:
To install our software first you need to clone the repository using the command `git clone https://github.com/Siggy13/NLPAttack.git`.
Then install the requirements in the requirements.txt file. From the command line change your directory to be the NLP directory andrun the
command `python3 manage.py runserver`. Finally, and go to the address 'http://127.0.0.1:8000/AdversarialTool/' in your web browser. The home
page for the software should appear. 


## How to Use the website
Once you are on the webpage the first screen you see will is our stress-based tool for demonstrating adversarial attacks. 
You can type text into the textbox on the homepage and click the 'Classify and Attack' button. The text will be classified as 'Stressed' or 'Not Stressed"
and an altered text will be provided;if the attack succeeds, the new text will be classified differently than the original text, and it will ideally have a 
similar meaning and make grammatical sense.
You can try out different attacks, besides the default, <a href="https://openattack.readthedocs.io/en/latest/apis/attacker.html#bertattacker">BERTAttacker,</a>
by clicking on the drop-down menu, selecting a new attack, and clicking the 'Classify and Attack" button again. This feature is particularly useful if one attack 
fails to find an appropriate replacement for the text, since a different attack might give better results. A very similar tool to the stress-based toolcan be 
found by clicking the “emotion based tool” tab on the header. This tool is used in exactly the same way as the stress-based tool but with different classifications
for the text. If a user wants to save any of the attacks they create,  they need to sign-up for an account. 

To sign-up, go to the login page, found in the header, type in a username and password, and click sign up. Once you have a valid account, a “Save Attack” button 
will appear under every successful attack. Once logged in you can save attacks and view all your saved attacks on the page in the header titled 
'Saved Attacks.' In the website’s footer, there are informational pages for the you to learn more about the project, the attacks, and how to use the tools.

