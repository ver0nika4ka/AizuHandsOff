from django.shortcuts import render
from django.http import HttpResponse

import datetime
from HandsOffApp.models import Owner, Category, Item


# Create your views here.
def main(request):
    response = "<h1>Welcome to Aizu HandsOff website!</h1>"

    all_items = Item.objects.all()

    response += "<h2>All items:</h2>"

    for item in all_items:
        response += "{}<br>".format(item)

    return HttpResponse(response)


def register(request):
    return HttpResponse('register')


def do_register(request):
    return HttpResponse('do_register')


def do_login(request):
    return HttpResponse('do_login')


def do_logout(request):
    return HttpResponse('do_logout')


def add_new_item(request):
    return HttpResponse('add_new_item')


def do_add_new_item(request):
    return HttpResponse('do_add_new_item')


def remove_item(request):
    return HttpResponse('remove_item')


def do_remove_item(request):
    return HttpResponse('do_remove_item')


def added_items(request):
    # Hardcode user email for now
    user_email = "veranika.aizu@gmail.com"
    # Получим юзера, чей email совпадает со строкой выше
    user = Owner.objects.filter(email=user_email).get()
    # Получим список items у которых owner - юзер полученный выше
    user_items = Item.objects.filter(owner=user)

    response = "<h2>Your list of added items:</h2>"
    for item in user_items:
        response += "{}<br>".format(item.name)

    return HttpResponse(response)
