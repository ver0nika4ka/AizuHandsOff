from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

import datetime
from HandsOffApp.models import Owner, Category, Item
from HandsOffApp.forms import RegisterForm, LoginForm, AddItemForm


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


def login(request):
    return render(request, 'login.html', {'login_form': LoginForm()})


def do_login(request):
    # Create form with data from the request(email and password)
    form = LoginForm(request.POST)

    try:
        if not form.is_valid():
            raise RuntimeError("Error: " + str(form.errors))
        values = form.cleaned_data

        # Receiving the list of users from database
        result = Owner.objects.filter(email=values['email'])
        if not result:
            # User with such email does not exist
            raise RuntimeError('Wrong email or password. Please try again.')

        user = result.get()

        if not check_password(values['password'], user.password):
            raise RuntimeError('Wrong email or password. Please try again.')
        # Create key-value in dictionary session
        # key "authorized_user_login" and value user email
        request.session['authorized_user_email'] = user.email
    except RuntimeError as e:
        return HttpResponse(str(e) + '<p><a href=login>Go back to login</a></p>')

    return redirect('my_items')


def do_logout(request):
    request.session['authorized_user_email'] = None
    return redirect('view-main')


def add_item(request):
    # if request.session['authorized_user_login'] == None:
    if not request.session.get('authorized_user_email'):
        return redirect('login')
    # Get category names
    category_names = [c.name for c in Category.objects.all()]
    form = AddItemForm(category_names=category_names)
    return render(request, 'add_item.html', {'add_item_form': form})


def do_add_item(request):
    # Pre-filled form with data what we got from add_item
    category_names = [c.name for c in Category.objects.all()]
    form = AddItemForm(request.POST, category_names=category_names)
    if not form.is_valid():
        raise RuntimeError('Error: ' + str(form.errors))
    values = form.cleaned_data
    user_email = request.session['authorized_user_email']
    # Get a user whose email matches with a line above
    user = Owner.objects.filter(email=user_email).get()
    # Get category name from database
    c = Category.objects.filter(name=values['category']).get()
    Item.objects.create(owner=user, category=c,
                        name=values['name'], description=values['description'],
                        available_date=values['available_date'], price=values['price'])

    return redirect('my_items')


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
