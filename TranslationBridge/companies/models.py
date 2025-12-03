from django.db import models


# Create your models here.

 
class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to="flags/", null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
        
    
    
class Language(models.Model):
    name= models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TranslatorAccreditation(models.Model):
    company= models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='accreditations'
        )
    date = models.DateField()
    month = models.CharField(max_length=20)
    
class Company(models.Model):
   
    name = models.CharField(max_length=200, unique=True)
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

    def __str__(self):
        return f"{self.name} - {self.rating} stars"

        

        