from typing import Tuple
from django.db import models
from account.models import User

class languages(models.TextChoices):
    ES = "Español"
    EN = "English"


class WordTerm(models.Model):
    # new_id = models.IntegerField(auto_created=True, unique=True, primary_key=True)
    word = models.CharField(max_length=200, unique=True)
    language = models.CharField(
        max_length=50, choices=languages.choices, blank=True, null=True)
    # translate = models.ManyToManyField('self', blank=True)
    # sinonyms = models.ManyToManyField('self', blank=True)
    phrase = models.BooleanField(default=False)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        correct = self.word.strip()
        correct.replace(',','')
        correct.replace('.','')
        
        self.word = correct
        super(WordTerm, self).save(*args, **kwargs)



class FlashCard(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_book')
    terms = models.ForeignKey(
        WordTerm, on_delete=models.CASCADE, related_name='users')

    # last calidad
    easiness = models.DecimalField(default=0, decimal_places=2, max_digits=4)

    last_review = models.DateField(null=True, blank=True)
    interval = models.IntegerField(default=0)
    repetitions = models.IntegerField(default=0)
    next_review_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} {self.terms.word}'
