from django.contrib import admin
from .models import Discount, Coupon

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'percentage', 'expiry_date', 'is_active')
    search_fields = ('code',)
    list_filter = ('is_active', 'expiry_date')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'user_eligibility', 'expiry_date')
    search_fields = ('code',)
    list_filter = ('user_eligibility', 'expiry_date')