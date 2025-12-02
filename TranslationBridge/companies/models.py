from django.db import models


# Create your models here.

 
class Country(models.Model):
    name = models.CharField(max_length=100, default="none")
    flag = models.ImageField(upload_to="images/", null=True, blank=True)

    
    
class City(models.Model):
    name = models.CharField(max_length=100, default="none")
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
        
    
    
class Language(models.Model):
    name= models.CharField(max_length=100, default="none")

    
class Company(models.Model):
    name = models.CharField(max_length=200, default="none")
    description = models.TextField(blank=True, null=True)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    languages = models.ManyToManyField(Language, blank=True)


    class RatingChoices(models.IntegerChoices):
        STAR1 = 1, '⭐'
        STAR2 = 2, '⭐⭐'
        STAR3 = 3, '⭐⭐⭐'
        STAR4 = 4, '⭐⭐⭐⭐'
        STAR5 = 5, '⭐⭐⭐⭐⭐'

    rating = models.SmallIntegerField(
        choices=RatingChoices.choices,
        default=RatingChoices.STAR5
    )

        

        