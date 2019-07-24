from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

import datetime
from HandsOffApp.models import Owner, Category, Item
from HandsOffApp.forms import RegisterForm, LoginForm, ItemForm


# Create your views here.
def main(request):
    all_items = Item.objects.all()
    category_list = Category.objects.all()
    # Check if the user is logged in
    is_authorized = True if request.session.get('authorized_user_email') else False
    message = 'All available items:'
    dictionary = {'items_list': all_items, 'sub_header': message,
                  'is_authorized': is_authorized, 'category_list': category_list}
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


def logout(request):
    request.session['authorized_user_email'] = None
    return redirect('view-main')


def add_item(request):
    # if request.session['authorized_user_login'] == None:
    if not request.session.get('authorized_user_email'):
        return redirect('login')
    form = ItemForm()
    return render(request, 'add_item.html', {'add_item_form': form})


def do_add_item(request):
    # Pre-fill form with data what we got from add_item
    form = ItemForm(request.POST)
    if not form.is_valid():
        raise RuntimeError('Error: ' + str(form.errors))
    item = form.save(commit=False)
    item.owner = get_user_or_show_login(request)
    # Save Item to the database
    item.save()
    return redirect('my_items')


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    dictionary = {'item': item}
    # Check if the user is logged in
    user_email = request.session.get('authorized_user_email')
    # and if item belongs to owner
    if user_email and item.owner.email == user_email:
        dictionary['is_authorized'] = True

    return render(request, 'item_detail.html', dictionary)


def edit_item(request, pk):
    user = get_user_or_show_login(request)
    item = get_object_or_404(Item, pk=pk, owner=user)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if not form.is_valid():
            raise RuntimeError('Error: ' + str(form.errors))
        form.save()
        # TODO: Check if required to set owner again
        return redirect('item_detail', pk=item.pk)
    else:
        # Create and pre-fill form based on item
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'edit_item_form': form})


def remove_item(request, pk):
    # Check if the user authorized and it is his item
    user = get_user_or_show_login(request)
    item = get_object_or_404(Item, pk=pk, owner=user)
    item.delete()
    return redirect('my_items')


def added_items(request):
    # Check if the user authorized and it is his item
    user = get_user_or_show_login(request)
    # Get the list of items where owner - a user from line above
    user_items = Item.objects.filter(owner=user)
    category_list = Category.objects.all()
    message = 'Your list of added items:'
    dictionary = {'items_list': user_items, 'sub_header': message,
                  'category_list': category_list, 'is_authorized': True}
    return render(request, 'items_list.html', dictionary)


def show_by_category(request, pk):
    # Get the category by pk (primary key)
    category = get_object_or_404(Category, pk=pk)
    # filter items by desired category
    items = Item.objects.filter(category=category)
    if items:
        message = "Items in category " + category.name
    else:
        message = "There are no items in category " + category.name
    dictionary = {'items_list': items, 'sub_header': message, 'category_list': Category.objects.all() }
    return render(request, 'items_list.html', dictionary)


def get_user_or_show_login(request):
    # Receiving user email from session 'authorized_user_email'
    user_email = request.session.get('authorized_user_email')
    if not user_email:
        return redirect('login')
    # Get a user whose email matches with a line above
    user = Owner.objects.filter(email=user_email).get()
    return user
