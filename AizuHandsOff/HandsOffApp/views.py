from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

import datetime
from HandsOffApp.models import Owner, Category, Item
from forms import RegisterForm


# Create your views here.
def main(request):
    all_items = Item.objects.all()
    message = 'All available items:'
    dictionary = {'items_list': all_items, 'sub_header': message}
    return render(request, 'items_list.html', dictionary)


def register(request):
    return render(request, 'register.html', {'register_form': RegisterForm()})


def do_register(request):
    form = RegisterForm(request.POST)
    try:
        if not form.is_valid():
            raise RuntimeError("Error: " + str(form.errors))
        # If form is valid, clean values are stored in cleaned_data field
        values = form.cleaned_data
        # Check the owner email in database if exist - error
        if len(Owner.objects.filter(email=values['email'])) > 0:
            raise RuntimeError("A user with the login {} already exists".format(values['email']))
        if values['password'] != values['passagain']:
            raise RuntimeError("Passwords do not match")

        Owner.objects.create(name=values['name'], email=values['email'],
                             password=make_password(values['password']),
                             contact_info=values['contact_info'])

    except RuntimeError as e:
        return HttpResponse(str(e) + "<p><a href=register>Go back</a></p>")
    return redirect('view-main')



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
