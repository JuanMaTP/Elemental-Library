from django.contrib.auth.models import User
from django.db import models

from general.constants import Gender, Type


class Person(models.Model):

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='person'
                                )

    birth_date = models.DateField()
    gender = models.CharField(max_length=Gender.GENDER_CHAR_LENGTH, choices=Gender.GENDER_CHOICES, default=Gender.MALE)
    type = models.CharField(max_length=Type.TYPE_CHAR_LENGTH, choices=Type.TYPE_CHOICES, default=Type.VISITOR)
    picture = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['gender']
