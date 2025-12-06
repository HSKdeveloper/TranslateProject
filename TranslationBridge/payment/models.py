from django.db import models
from django.contrib.auth.models import User
from translation_request.models import TranslationRequest

# Create your models here.

class Payment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_payments")
    request = models.OneToOneField(TranslationRequest, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for Request {self.request.id}"

    