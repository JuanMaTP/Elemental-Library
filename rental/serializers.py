from django.utils import timezone
from rest_framework import serializers

from person.models import Person

from .models import Rental


class RentalSerializer(serializers.ModelSerializer):

    return_date = serializers.DateTimeField(read_only=True)
    rental_date = serializers.DateTimeField(read_only=True)
    person_type = serializers.CharField(read_only=True)
    person = serializers.CharField(read_only=True)

    class Meta:
        model = Rental

        fields = '__all__'

    def validate_book_unit(self, book_unit):
        if book_unit.borrowed:
            raise serializers.ValidationError('Book is currently borrowed')
        return book_unit

    # The person and their type come from the logged-in user, not from the request body
    def create(self, validated_data):
        user = self.context['request'].user
        try:
            person = user.person
        except Person.DoesNotExist:
            raise serializers.ValidationError('Only registered people can borrow books')

        validated_data['person'] = person
        validated_data['person_type'] = person.type

        return Rental.objects.create(**validated_data)


# Serializer to use when a BookUnit is returned
class RentalReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rental

        fields = ['id', 'book_unit', 'rental_date', 'return_date']
        read_only_fields = fields

    # A PUT to the return endpoint sets the return date to now, once
    def update(self, instance, validated_data):
        if instance.return_date is None:
            instance.return_date = timezone.now()
            instance.save()

        return instance
