from rest_framework import serializers
from models import Listing, User

class ListingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Listing
		fields = ('fulfillment_partner', 'address', 'radius', 'phone_number', 'active')
		data = {'fulfillment_partner': User} # need to submit the form with the User. This doesn't right. Currently it's a choice field showing all users.

	