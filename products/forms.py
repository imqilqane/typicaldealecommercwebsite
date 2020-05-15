from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

CHOISES =(
    ('P','Paypal'),
    ('S','Stripe')
)
class CheckoutForm(forms.Form):
    #shipping adress
    shipping_adress1 = forms.CharField(max_length=300,required=False)
    shipping_adress2 = forms.CharField(max_length=300, required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id':'country',
        'name':'country'
    }),required=False)
    shipping_zip_code = forms.CharField(required=False, max_length=100 )
    use_same_shipping_adresse = forms.BooleanField(required=False)
    save_shipping_adress = forms.BooleanField(required=False)
    use_default_shipping_adress = forms.BooleanField(required=False)

    #Billing adress
    adress1 = forms.CharField(max_length=300, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'address',
        'placeholder':'1234 Main St',
        'name':'adress1'
    }),required=False)
    adress2 = forms.CharField(max_length=300, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'address',
        'placeholder':'Apartment or suite',
        'name':'adress2'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id':'country',
        'name':'country'
    }),required=False)
    zip_code = forms.CharField(max_length=100,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id':'zip',
        'placeholder':'Enter Zip',
        'name':'zip_code'
    }),required=False)
    save_adress_as_default = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False,)
    payment_method = forms.ChoiceField(choices=CHOISES ,widget=forms.RadioSelect(attrs={
          
    }),required=False)

class CouponCodeForm(forms.Form):
     code = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Promo code',
        'class':'form-control',
    }))

class refundForm(forms.Form):
    email = forms.EmailField()
    order_number = forms.CharField(max_length=20)
    reason = forms.CharField(widget=forms.Textarea())


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save_billing = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)