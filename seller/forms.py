from datetime import date, datetime
from calendar import monthrange

from django import forms
from .models import *


class AddressForm(forms.Form):	
    address = forms.CharField()
    

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['first_name', 'email', 'address', 'phone', 'radius', 'open_hour', 'close_hour', 'item', 'unit_price', 'picture', 'description', 'min_order_amount', 'license_number', 'license_exp', 'operating_days']		
        widgets = {
            'first_name': forms.TextInput(
                attrs={'readonly': True, 'class': 'form-control'}
            ),
            'email': forms.TextInput(
                attrs={'readonly': True, 'class': 'form-control'}
            ),
            'address': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'phone': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'radius': forms.TextInput(
                attrs={'class': 'form-control'}
            ),        
            'open_hour': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'close_hour': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'item': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),            
            'unit_price': forms.TextInput(
                attrs={'required': True, 'class': 'form-control'}
            ),
            'description': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'license_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'license_exp': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'operating_days': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'first_name': 'Name',
            'license_exp': 'License Expiration',
            'unit_price': 'Unit Price in Cents',
        }
	
#################################################################################
# buyer charge form.                                                            #
# it may be easier to use the stripe api instead of this and I'm concerned      #
# about                                                                         #
# PCI compliance and don't want to store any credit card information.           #
# Need to add Stripe Connect 'application_fee'                                  #
# Need to populate customer_token for Buyer and 'destination' for Seller.       #
# Need to integrate a sales tax api with Stripe, like Avalara or TaxCloud.      #
# want sales tax to be collected and reported by Seller so it should go to      #
# 'destination'.                                                                #
################################################################################
        
class OrderForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Seller Name')
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Seller Email')
    address = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'required': True, 'class': 'form-control'}), label='Customer Location')
    unit_price = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label="Unit Price in Cents")
    min_order_amount = forms.FloatField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label="Min. Quantity of Units")	
    quantity = forms.FloatField(widget=forms.NumberInput(attrs={'required': True, 'class': 'form-control'}), label="Quantity of Units")
    buyer_name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}), label="Buyer Name")
    buyer_phone = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}),label="Buyer Phone Number")

    		  