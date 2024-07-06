from django.contrib import admin

from shop.models import Category, Product, ProductImage, ProductVideo, CartItem, Cart, ShippingAddress, OrderItem, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVideo)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Cart)
admin.site.register(CartItem)
