from django.shortcuts import render, redirect
from django.urls import reverse

from . import models



def decode(request, message):
    return render(request, "decode.html")

def index(request):
    content = "Hier kann man Texte verschlüsseln."
    return render(request, "home.html", {
        "content": content
    })


def load_secretnote(request, uuid):
    try:
        content = "Deine Geheime Nachricht ist."
        secretnote = models.SecretMsg.objects.get(uuid=uuid)
    except:
        return render(request, "home.html")

    return render(request, "home.html", {
        "secretnote": secretnote,
        "content": content
    })


def create_secretnote(request):
    if request.method == "GET":
        return redirect(reverse("home"))
    if request.method == "POST":
        # write action
        # wir erzeugen einen Datenbankeintrag mit dem selbstgebauten model
        # sowie Djangos Framework
        secret_message = models.SecretMsg.objects.create(
            message=request.POST.get("message")
        )
        # wir setzten/speichern den Datenbakeintrag
        # ohne diesen Befehl ist der vorangegangene Befehl nutzlos(ohne Effekt auf die Datenbank)
        secret_message.save()
        return render(request, "create_success.html", {
            "secret_message": secret_message
        })

def encode_decode(request):
    status_decode = request.POST.get("decode")
    status_encode = request.POST.get("encode")
    input = request.POST.get("message")

    if status_encode:
    # encode action
        secret_message = models.SecretMsg.objects.create(
        message=input
        )
        secret_message.save()
        return render(request, "home.html", {
            "secretnote": secret_message.uuid,
            "content": "Gespeichert"
             })
    elif status_decode:
    # decode action
        try:
            secretnote = models.SecretMsg.objects.get(uuid=input)
        except:
            content = "Diese Nachricht existiert nicht"
            return render(request, "home.html",{
                "content": content

            })

        return render(request, "home.html", {
            "secretnote": secretnote.message,
            "content": "Deine Nachricht  ist:"
            })

    else:
    # no button pressed
        return
    return render(request, "home.html")
