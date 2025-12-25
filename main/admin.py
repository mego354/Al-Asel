from django.contrib import admin

from .models import Customer, Order, Item, OrderItem, Category, Store_Order, Store_OrderItem, OrderPayment, SupplyTransaction


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id","quantity", "item", "order", "profit")

class Store_OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id","quantity", "item", "order", "total_real_price", "total_gomla_price", "total_market_price")

class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "real_price", "gomla_price", "market_price", "quantity")
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "total_order_price", "is_fully_paid", "rest_money", "discount", "profit", "created_at")
        

class Store_OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "supplier", "total_order_price", "is_fully_paid", "rest_money", "created_at") 

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)

admin.site.register(Store_OrderItem, Store_OrderItemAdmin)
admin.site.register(Store_Order, Store_OrderAdmin)

admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)

@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('order__id', 'amount')

@admin.register(SupplyTransaction)
class SupplyTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'value', 'date')
    list_filter = ('date',)
    search_fields = ('order__id', 'value')


# Register your models here.
