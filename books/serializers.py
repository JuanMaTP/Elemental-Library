from django.utils.crypto import get_random_string
from rest_framework import serializers

from author.serializers import AuthorViewSerializer

from .models import Book, BookUnit


class BookSerializer(serializers.ModelSerializer):
    # author = AuthorViewSerializer(many=True, required=False)

    class Meta:
        model = Book

        fields = '__all__'


class BookUnitSerializer(serializers.ModelSerializer):

    serial = serializers.CharField(min_length=16, max_length=16)
    book = BookSerializer(read_only=True)
    borrowed = serializers.BooleanField(read_only=True)

    class Meta:
        model = BookUnit

        fields = '__all__'

    def create(self, validated_data):
        if 'serial' not in validated_data:
            validated_data['serial'] = get_random_string(length=16)

        return BookUnit.objects.create(**validated_data)


# Serializer used to show Book information, but also allow creation of BookUnit
class BookAddUnitSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    author = AuthorViewSerializer(many=True, required=False)
    book_units = BookUnitSerializer(many=True, read_only=True)
    serial = serializers.CharField(min_length=16, max_length=16, required=False)

    class Meta:
        model = Book

        fields = '__all__'

    # Modify fields properties depending on the HTTP Method
    def get_fields(self, *args, **kwargs):
        fields = super(BookAddUnitSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        # if the method is POST, make name, description and author read_ony
        if request and getattr(request, 'method', None) == "POST":
            fields['name'].read_only = True
            fields['description'].read_only = True
            fields['author'].read_only = True
        if request and getattr(request, 'method', None) == "PUT":
            fields['serial'].read_only = True
        return fields
