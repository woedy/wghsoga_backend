
from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import Category, Product, Order, OrderItem


class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"






class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"



class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"






class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"



class AllOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"



class OrderItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"



class AllOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"