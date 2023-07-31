from rest_framework import serializers
from . models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(source='category.title', read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    menuitem_id = MenuItemSerializer(write_only=True)
    user_id = UserSerializer(write_only=True)   
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price', 'user_id', 'menuitem_id']

    # class Meta:
    #     model = Cart
    #     fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField(source='menuitem.title')
    
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']


