from django.db import models


# Create your models here.
#class Country(models.Model):
   # name = models.CharField(max_length=200, unique= True)
    #flag = models.ImageField(upload_to="images/")

#class City(models.Model):
   # name = models.CharField(max_length=200, unique= True)
    #one to many relationship
   # country = models.ForeignKey( Country, on_delete= models.CASCADE)

#class Language(models.Model):
       # name = models.CharField(max_length=200)


#class Company(models.Model):
       # user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
        #type = models.CharField(max_length=2000)
       # description = models.TextField(blank=True, null=True)
        #word_number = models.IntegerField(default=0) عدد الكلمات التي تمت ترجمتها من قبل الشركة
        #final_date = models.DateTimeField(blank=True, null=True)
        #cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        #file = models.FileField(upload_to=0)
       # languages = models.ManyToManyField(Language)

        #class RatingChoice(models.IntegerChoices):
               # STAR1 = 1, 'One Star'
              #  STAR2 = 2, 'Two Stars'
               # STAR3 = 3, 'Three Stars'
                #STAR4 = 4, 'Four Stars'
               # STAR5 = 5, 'Five Stars'

        #rating = models.SmallIntegerField(choices=RatingChoice.choices)

#class CompanyReview(models.Model):
       # name = models.CharField(max_length=1024)
        #rating = models.SmallIntegerField()
       # comment = models.TextField()
       # created_at = models.DateTimeField(auto_now_add=True)

        #one to many relationship
       # company = models.ForeignKey(Company, on_delete=models.CASCADE)#