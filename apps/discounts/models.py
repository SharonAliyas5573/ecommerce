from django.db import models
from django.utils import timezone

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return self.is_active and self.expiry_date > timezone.now()

    def __str__(self):
        return self.code

class Coupon(models.Model):
    discount = models.ForeignKey(Discount, related_name='coupons', on_delete=models.CASCADE)
    user_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)

    def can_use(self):
        return self.used_count < self.user_limit

    def __str__(self):
        return f'Coupon for {self.discount.code}'