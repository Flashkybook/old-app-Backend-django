from rest_framework import serializers
from .models import UserBook, WordTerm


class WordTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordTerm
        fields = '__all__'


class UserBookSerializer(serializers.ModelSerializer):
    # debe llamarse user_book.terms
    terms = WordTermSerializer()

    class Meta:
        model = UserBook
        fields = ('terms', 'easiness', 'interval', 'repetitions',
                  'last_review', 'next_review_date',  'user', 'id', )
