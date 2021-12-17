from django.urls import path
from . import views

app_name = "AdversarialTool"
urlpatterns=[
    path("",views.index, name="index"),
    path("emotions",views.emotions, name="emotions"),
    path("FAQ",views.FAQ, name="FAQ"),
    path("examples",views.examples, name="examples"),
    path("github",views.FAQ, name="FAQ"),
    path("about",views.about, name="about"),
    path("aboutAttacks",views.aboutAttacks, name="aboutAttacks"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("savedAttacks", views.savedAttacks, name="savedAttacks"),
    path("delete_attack/<attack_id>", views.delete_attack, name="delete_attack"),

    
]