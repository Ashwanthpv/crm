from rest_framework import serializers
from .models import Customer, Interaction, Task, Deal, Product


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'customer', 'date', 'note']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'customer', 'status', 'due_date', 'created_at', 'updated_at']


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['id', 'title', 'description', 'customer', 'amount', 'status', 'expected_close', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'sku', 'in_stock', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    deals = DealSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'company', 'product', 'status', 'description', 'assignee', 'next_step', 'created_at', 'interactions', 'tasks', 'deals']
