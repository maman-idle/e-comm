from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'status',
                    'order_date', 'quantity', 'price_sum')
    search_fields = ('customer__username', 'product__name', 'status',)
    readonly_fields = ('order_date', 'quantity')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'address', 'phone',
                    'last_login', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'address',)
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        ('Account Info', {'fields': ('username',
         'email', 'address', 'phone', 'date_joined')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'group',)}),
    )


admin.site.register(Account, AccountAdmin)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
