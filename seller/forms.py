from django import forms
from models import Listing, Sale


#################################################################################
# fulfilment partner form														#
# it would be ideal to get some of this populated from Stripe Connect response.	#
# also it may need lat lng and address fields, but didn't add because haven't 	#
# figured that out yet.															#
# need to add file upload with size limits so Fulfillment Partner can upload 	#
# County Health Inspector's License. 											#
# need to add min quantity order and max quantity order and unit price fields. 	#
# can't set price for each fulfillment partner as that may be violate anti-trust#
# laws.																			#
#################################################################################
class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ['fulfillment_partner', 'address', 'phone_number', 'active']		

		

#################################################################################
# buyer charge form.															#
# it may be easier to use the stripe api instead of this and I'm concerned 		#
# about																			#
# PCI compliance and don't want to store any credit card information.			#
# Need to add Stripe Connect 'application_fee'									#
# Need to populate customer_token for Buyer and 'destination' for Seller.		#
# Need to integrate a sales tax api with Stripe, like Avalara or TaxCloud.		#
# want sales tax to be collected and reported by Seller so it should go to 		#
# 'destination'.																#
################################################################################
		
# stripe charge form
# source: http://bryanhelmig.com/20-minutes-with-stripe-and-django/
from datetime import date, datetime
from calendar import monthrange
 
class CreditCardField(forms.IntegerField):
    def clean(self, value):
        """Check if given CC number is valid and one of the
           card types we accept"""
        #if value and (len(value) &lt; 13 or len(value) &gt; 16):
        #    raise forms.ValidationError("Please enter in a valid "+\
        #        "credit card number.")
        return super(CreditCardField, self).clean(value)
 
class CCExpWidget(forms.MultiWidget):
    """ Widget containing two select boxes for selecting the month and year"""
    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]
 
    #def format_output(self, rendered_widgets):
    #    html = u' / '.join(rendered_widgets)
    #    return u'<span style="white-space: wrap;">%s</span>' % html
 
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
        #if date.today() &gt; exp:
        #    raise forms.ValidationError(
        #    "The expiration date you entered is in the past.")
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
 
class SalePaymentForm(forms.Form):
	number = CreditCardField(required=True, label="Card Number")
	expiration = CCExpField(required=True, label="Expiration")
	cvc = forms.IntegerField(required=True, label="CCV Number", 
		max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))
	
	def clean(self):
		cleaned = super(SalePaymentForm, self).clean()
		
		if not self.errors:
			number = self.cleaned_data["number"]
			exp_month = self.cleaned_data["expiration"].month
			exp_year = self.cleaned_data["expiration"].year
			cvc = self.cleaned_data["cvc"]
			
			sale = Sale()
			
			# let's charge $10.00 for this particular item
			success, instance = sale.charge(1000, number, exp_month, exp_year, cvc)
			
			if not success:
				raise forms.ValidationError("Error: %s" % instance.message)
			else:
				instance.save()
                # we were successful! do whatever you will here...
                # perhaps you'd like to send an email...
                pass
		return cleaned