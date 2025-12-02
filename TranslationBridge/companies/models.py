from django.db import models

# Create your models here.
class Company(models.Model):
        user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
        type = models.CharField(max_length=2000)
        description = models.TextField(blank=True, null=True)
        #word_number = models.IntegerField(default=0) عدد الكلمات التي تمت ترجمتها من قبل الشركة
        final_date = models.DateTimeField(blank=True, null=True)
        cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
        file = models.FileField(upload_to=0)
        

        class LanguageChoice(models.TextChoices):
                ARABIC = 'arabic', 'Arabic'
                ENGLISH = 'english', 'English'
                KOREAN = 'korean', 'Korean'
                CHINESE = 'chinese', 'Chinese'
                JAPANESE = 'japanese', 'Japanese'
                OTHER = "other", "Other"

        languages = models.CharField(max_length=50, choices=LanguageChoice.choices)

        class RatingChoice(models.IntegerChoices):
                STAR1 = 1, 'One Star'
                STAR2 = 2, 'Two Stars'
                STAR3 = 3, 'Three Stars'
                STAR4 = 4, 'Four Stars'
                STAR5 = 5, 'Five Stars'

        rating = models.SmallIntegerField(choices=RatingChoice.choices)

