from django.test import TestCase
from .models import Discount, Coupon

class DiscountModelTests(TestCase):

    def setUp(self):
        self.discount = Discount.objects.create(
            code='SUMMER21',
            percentage=20,
            expiry_date='2023-12-31',
            is_active=True
        )

    def test_discount_creation(self):
        self.assertEqual(self.discount.code, 'SUMMER21')
        self.assertEqual(self.discount.percentage, 20)
        self.assertTrue(self.discount.is_active)

    def test_discount_expiry(self):
        self.discount.expiry_date = '2021-12-31'
        self.discount.save()
        self.assertFalse(self.discount.is_active)

class CouponModelTests(TestCase):

    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='WELCOME10',
            discount_amount=10,
            expiry_date='2023-12-31',
            is_valid=True
        )

    def test_coupon_creation(self):
        self.assertEqual(self.coupon.code, 'WELCOME10')
        self.assertEqual(self.coupon.discount_amount, 10)
        self.assertTrue(self.coupon.is_valid)

    def test_coupon_expiry(self):
        self.coupon.expiry_date = '2021-12-31'
        self.coupon.save()
        self.assertFalse(self.coupon.is_valid)