from datetime import date, datetime
from calendar import monthrange

from django import forms
from .models import *


class AddressForm(forms.Form):	
    address = forms.CharField()
    

class SellerForm(forms.ModelForm):
	class Meta:
		model = Seller
		fields = ['id', 'name', 'address', 'phone', 'radius', 'open_hour', 'close_hour', 'item', 'unit_price', 'picture', 'description', 'min_order_amount',
		'license_number', 'license_exp', 'operating_days']		

	
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
        
# stripe charge form
# source: http://bryanhelmig.com/20-minutes-with-stripe-and-django/
 
class CreditCardField(forms.IntegerField):
    def clean(self, value):
        """Check if given CC number is valid and one of the
           card types we accept"""
        if value and (len(value) < 13 or len(value) > 16):
           raise forms.ValidationError("Please enter in a valid "+\
               "credit card number.")
        return super(CreditCardField, self).clean(value)

 
class CCExpWidget(forms.MultiWidget):
    """ Widget containing two select boxes for selecting the month and year"""
    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]
 
    def format_output(self, rendered_widgets):
       html = u' / '.join(rendered_widgets)
       return u'<span style="white-space: wrap;">%s</span>' % html

 
class CCExpField(forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in xrange(1, 13)]
    EXP_YEAR = [(x, x) for x in xrange(date.today().year,
                                       date.today().year + 15)]
    default_error_messages = {
        'invalid_month': u'Enter a valid month.',
        'invalid_year': u'Enter a valid year.',
    }
 
    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.ChoiceField(choices=self.EXP_MONTH,
                error_messages={'invalid': errors['invalid_month']}),
            forms.ChoiceField(choices=self.EXP_YEAR,
                error_messages={'invalid': errors['invalid_year']}),
        )
        super(CCExpField, self).__init__(fields, *args, **kwargs)
        self.widget = CCExpWidget(widgets =
            [fields[0].widget, fields[1].widget])
 
    def clean(self, value):
        exp = super(CCExpField, self).clean(value)
        if date.today() > exp:
           raise forms.ValidationError(
           "The expiration date you entered is in the past.")
        return exp
 
    def compress(self, data_list):
        if data_list:
            if data_list[1] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if data_list[0] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)
            year = int(data_list[1])
            month = int(data_list[0])
            # find last day of the month
            day = monthrange(year, month)[1]
            return date(year, month, day)
        return None

class OrderForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Seller Name')
	id = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label='Seller ID')
	address = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'required': True, 'class': 'form-control'}), label='Customer Location')
	unit_price = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label="Unit Price in Cents")
	min_order_amount = forms.FloatField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}), label="Min. Quantity of Units")	
	quantity = forms.FloatField(widget=forms.NumberInput(attrs={'required': True, 'class': 'form-control'}), label="Quantity of Units")
	buyer_name = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}), label="Buyer Name")
	buyer_phone = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}),label="Buyer Phone Number")
	number = CreditCardField(widget=forms.TextInput(attrs={'required': True, 'class': 'form-control'}),required=True, label="Card Number")
	expiration = CCExpField(required=True, label="Expiration")
	cvc = forms.IntegerField(required=True, label="CVC Number", max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))
	
	def clean(self):
		cleaned = super(OrderForm, self).clean()
		
		if not self.errors:
			number = self.cleaned_data["number"]
			exp_month = self.cleaned_data["expiration"].month
			exp_year = self.cleaned_data["expiration"].year
			cvc = self.cleaned_data["cvc"]
			seller = self.cleaned_data['name'] # getting error here. 
			sale = Sale()
			
			success, instance = sale.charge(number, exp_month, exp_year, cvc)
			
			if not success:
				raise forms.ValidationError("Error: %s" % instance.message)
				
			else:
				instance.save()
				pass
			return cleaned

			