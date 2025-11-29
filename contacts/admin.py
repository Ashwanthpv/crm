from django.contrib import admin
from .models import Customer, Interaction, Task, Deal, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'company', 'created_at')


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'customer', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'due_date')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'customer', 'amount', 'status', 'expected_close', 'created_at')
    list_filter = ('status', 'expected_close')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'sku', 'in_stock', 'created_at')
