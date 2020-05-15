from django.contrib import admin
from .models import Product , Category , Cart , Order, Payment, Adresse, Coupon, Refund , User_profile
# Register your models here.

def bulk_accepte_refund(ModelAdmin, request, queryset):
    queryset.update(refund_accepted=True)
bulk_accepte_refund.short_description= 'mark refunds as accepted'

class AdresseAdmin(admin.ModelAdmin):
    list_display=[
        'user',
        'adress1',
        'adress2',
        'country',
        'zip_code',
        'adresse_type',
        'defualt',
    ]
    search_fields=[
        'user',
        'adress1',
        'adress2',
        'country',
        'zip_code',
        'adresse_type',
        'defualt',
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display=[
        'user',
        'ordered',
        'refunded_requested',
        'refund_accepted',
        'been_deliverd',
        'arrived',

        ]
    list_filter=[
        'refunded_requested',
        'refund_accepted',
        'been_deliverd',
        'arrived',
    ]
    actions = [bulk_accepte_refund,]

class CouponAdmin(admin.ModelAdmin):
    list_display=['code','amount','active']

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Adresse , AdresseAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Refund)
admin.site.register(User_profile)