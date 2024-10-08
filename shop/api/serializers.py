
from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import Category, Product, Order, OrderItem, ProductImage, ProductVideo


class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"






class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = "__all__"

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductDetailsSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()
    product_videos = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = "__all__"

            
    def get_product_images(self, obj):
        # Fetching only the 'photos' field from the Product Images model
        return obj.product_images.filter(is_archived=False).values_list('image', flat=True)


    def get_product_videos(self, obj):
        # Fetching only the 'videos' field from the Product Videos model
        return obj.product_videos.filter(is_archived=False).values_list('video', flat=True)






class AllProductSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = "__all__"


    def get_product_image(self, obj):
        product_image = obj.product_images.first()
        if product_image:
            return product_image.image.url
        return None






class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"



class AllOrdersSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"


        
    def get_product_name(self, obj):
        item = obj.items.first()
        if item:
            return item.product.name
        return None



        
    def get_product_image(self, obj):
        item = obj.items.first()
        if item:
            return item.product.product_images.first().image.url
        return None



        
    def get_customer_name(self, obj):
        customer = obj.customer
        if customer:
            return customer.first_name + " " + customer.last_name
        return None

    def get_quantity(self, obj):
        item = obj.items.first()
        if item:
            return item.quantity
        return None



    def get_price(self, obj):
        item = obj.items.first()
        if item:
            return item.price
        return None



class OrderItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"



class AllOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"