from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label='Name', max_length=64)
    email = forms.EmailField()
    password = forms.CharField(label='Password', max_length=20, widget=forms.PasswordInput)
    passagain = forms.CharField(label='Re-enter password', max_length=20, widget=forms.PasswordInput)
    # TODO: Add default text to the field, such as 'Please provide your contact information...'
    contact_info = forms.CharField(label='Your contact information', max_length=256)


class AddItemForm(forms.Form):
    name = forms.CharField(label='Item Name', max_length=64)
    description = forms.CharField(label='Item Description', max_length=512)
    available_date = forms.DateField(label='Item available from')
    price = forms.CharField(label='Input price or write Free', max_length=64)