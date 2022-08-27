from django.db import models
from django.utils.timezone import datetime


class City(models.Model):
    city = models.CharField(max_length=150)
    time_zone = models.DateField(default=datetime.now)
    value = models.IntegerField()
    # image = models.ImageField(
    #     upload_to="avatars",
    #     height_field=None,
    #     width_field=None,
    #     max_length=100,
    #     blank=True,
    # )


class Company(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    date_created = models.DateField()

    def __str__(self):
        return self.name


class Language(models.Model):

    name = models.CharField(max_length=20)
    creator = models.CharField(max_length=20)
    paradigm = models.CharField(max_length=20)
    date_created = models.DateField()

    def __str__(self):
        return self.name


class Programmer(models.Model):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=10,
        blank=True,
    )
    password = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="programmer",
    )
    languages = models.ManyToManyField(Language)

    def __str__(self):
        return self.name
