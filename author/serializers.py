from rest_framework import serializers

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author

        fields = '__all__'


class AuthorViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author

        fields = ['name', 'birth_date', 'gender']
