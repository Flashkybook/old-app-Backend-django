from django.db import models
# from django.contrib.auth.models import User
from account.models import User
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator

# PHRASE:
# tienen palabras, no tienen sinonimos, si esta en userbook, word es null, y si no esta es null

class WordTerm(models.Model):
    word = models.CharField(max_length=50, unique=True, primary_key=True)
    phrase = models.BooleanField(default=False)
    

    def __str__(self):
        return self.word


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_book')
    terms = models.ForeignKey(
        WordTerm, on_delete=models.CASCADE, related_name='users')
    # sinonyms = models.ManyToManyField('self')

    # last calidad
    easiness = models.PositiveIntegerField(default=5, validators=[MaxValueValidator(5),MinValueValidator(0) ])
    last_review  = models.DateField( null=True, blank=True)
    interval  = models.IntegerField( null=True, blank=True)
    repetitions  = models.IntegerField( null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} {self.terms.word} '
