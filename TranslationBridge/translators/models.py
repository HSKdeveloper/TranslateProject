from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#Translator location model
class Country(models.Model):
    name = models.CharField(max_length=200, unique= True)
    flag = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200, unique= True)
    #one to many relationship
    country = models.ForeignKey( Country, on_delete= models.CASCADE)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50, unique= True )

    def __str__(self):
        return self.name


#Translator information model
class Translator(models.Model):

    class RatingChoices(models.IntegerChoices):
        STAR1 = 1, "One Star"
        STAR2 = 2, "Two Stars"
        STAR3 = 3, "Three Stars"
        STAR4 = 4, "Four Stars"
        STAR5 = 5, "Five Stars"

    #user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    experience = models.TextField()
    rating = models.SmallIntegerField(choices=RatingChoices.choices, default=1)
    created_at = models.DateTimeField(auto_now=True)
    
    #location - one to many relationship
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    #add languages
    languages = models.ManyToManyField(Language)

    def __str__(self):
        return self.user


#Users review 
class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField( auto_now_add= True )

    #one to many relationship
    translator = models.ForeignKey( Translator, on_delete=models.CASCADE )

    def __str__(self):
        return f"{self.user.username} on {self.translator.user}"