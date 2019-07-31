from django import forms
# import ModelForm to map forms to Django models
from django.forms import ModelForm
from HandsOffApp.models import Item
from bootstrap_datepicker_plus import DatePickerInput
import datetime

ADVANCE_AVAILABILITY_DAYS = 90

class RegisterForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64)
    email = forms.EmailField()
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput)
    passagain = forms.CharField(label='Re-enter password', max_length=20, widget=forms.PasswordInput)
    # TODO: Add default text to the field, such as 'Please provide your contact information...'
    contact_info = forms.CharField(label='Your contact information', max_length=256)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput)


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'available_date', 'price']

        # TODO: Maybe, make date format as 'YYYY/MM/DD'
        datepicker_params = {
            'minDate': datetime.date.today().strftime('%m/%d/%Y'),
            'maxDate': (datetime.date.today() + datetime.timedelta(days=ADVANCE_AVAILABILITY_DAYS)).strftime('%m/%d/%Y'),
            'showTodayButton': True
        }
        widgets = {'available_date': DatePickerInput(options=datepicker_params)}

