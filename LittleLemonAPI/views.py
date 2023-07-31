from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, status
from rest_framework.views import APIView

from django.contrib.auth.models import User, Group

from django.db.models import Sum

from datetime import date

from rest_framework.authtoken.models import Token

from django.core.paginator import Paginator, EmptyPage



from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, CartSerializer, OrderItemSerializer, OrderSerializer

from . models import MenuItem, Category, Cart, Order, OrderItem

from rest_framework.permissions import IsAdminUser



# Create your views here.

@api_view()
@permission_classes([IsAdminUser])
def managers(request):
    return Response({"message": "ok"})





class CategoryListAPIView(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serialized_category = CategorySerializer(all_categories, many=True)
        return Response(serialized_category.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        if request.user.is_superuser:
            serialized_category = CategorySerializer(data=request.data)
            if serialized_category.is_valid():
                serialized_category.save()
                return Response({"message": "Category added", "category": serialized_category.data}, status=status.HTTP_200_OK)
            else:
                return Response(serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authorization is required"}, status=status.HTTP_403_FORBIDDEN)


class CategorySingleAPIView(APIView):

    def get(self, request, categoryId):
        selected_category = get_object_or_404(Category, id=categoryId)
        serialized_category = CategorySerializer(selected_category)
        return Response(serialized_category.data, status=status.HTTP_200_OK)


    @permission_classes([IsAuthenticated])
    def put(self,request, categoryId):
        selected_category = get_object_or_404(Category, id=categoryId)
        if request.user.is_superuser:
            serialized_category = CategorySerializer(selected_category, data=request.data)
            if serialized_category.is_valid():
                serialized_category.save()
                return Response({"message": "Category added", "category": serialized_category.data}, status=status.HTTP_200_OK)
            else:
                return Response(serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authorization is required"}, status=status.HTTP_403_FORBIDDEN)
    
    @permission_classes([IsAuthenticated])
    def patch(self, request, categoryId):
        selected_category = get_object_or_404(Category, id=categoryId)
        if request.user.is_superuser:
            serialized_category = CategorySerializer(selected_category, data=request.data, partial=True)
            if serialized_category.is_valid():
                serialized_category.save()
                return Response({"message": "Category updated", "category": serialized_category.data}, status=status.HTTP_200_OK)
            else:
                return Response(serialized_category.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Authorization is required"}, status=status.HTTP_403_FORBIDDEN)
        
    @permission_classes([IsAuthenticated])
    def delete(self, request, categoryId):
        selected_category = get_object_or_404(Category, id=categoryId)
        if request.user.is_superuser:
            selected_category.delete()
            return Response({"message": "Category Deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Authorization is required"}, status=status.HTTP_403_FORBIDDEN)
        



class MenuItemListAPIView(APIView):
    def get(self, request):
        all_MenuItems = MenuItem.objects.all()
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)

        if search:
            all_MenuItems = all_MenuItems.filter(title__icontains=search)

        if ordering:
            all_MenuItems = all_MenuItems.order_by(ordering)

        paginator = Paginator(all_MenuItems, per_page = perpage)
        try:
            all_MenuItems = paginator.page(number = page)
        except EmptyPage:
            all_MenuItems = []


        serialized_MenuItems = MenuItemSerializer(all_MenuItems, many=True)
        return Response(serialized_MenuItems.data)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            serialized_MenuItems = MenuItemSerializer(data = request.data)
            if serialized_MenuItems.is_valid():
                serialized_MenuItems.save()
                return Response(serialized_MenuItems.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serialized_MenuItems.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You Are Not Authorized"},status = status.HTTP_403_FORBIDDEN)
   

class MenuItemSingleAPIView(APIView):
    
    def get(self, request, menuItem):
        selected_MenuItem = get_object_or_404(MenuItem, pk=menuItem)
        serialized_MenuItem = MenuItemSerializer(selected_MenuItem)
        return Response(serialized_MenuItem.data, status=status.HTTP_200_OK)
        
    @permission_classes([IsAuthenticated])
    def put(self, request, menuItem):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            selected_MenuItem = get_object_or_404(MenuItem, pk=menuItem)
            serialized_MenuItem = MenuItemSerializer(selected_MenuItem, data=request.data)
            if serialized_MenuItem.is_valid():
                serialized_MenuItem.save()
                return Response(serialized_MenuItem.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized_MenuItem.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You Are Not Authorized"},status = status.HTTP_403_FORBIDDEN)
        
    @permission_classes([IsAuthenticated])
    def patch(self, request, menuItem):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            selected_MenuItem = get_object_or_404(MenuItem, pk=menuItem)
            serialized_MenuItem = MenuItemSerializer(selected_MenuItem, data=request.data, partial=True)
            if serialized_MenuItem.is_valid():
                serialized_MenuItem.save()
                return Response(serialized_MenuItem.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized_MenuItem.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You Are Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
        
    @permission_classes([IsAuthenticated])
    def delete(self, request, menuItem):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            selected_MenuItem = get_object_or_404(MenuItem, pk=menuItem)
            selected_MenuItem.delete()
            return Response({"message": "Menu item Deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"message": "You Are Not Authorized"},status = status.HTTP_403_FORBIDDEN)
        





class ManagerListAPIView(APIView):
    
    @permission_classes([IsAuthenticated])
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            managers_group = Group.objects.get(name='Manager')
            all_managers = User.objects.filter(groups=managers_group)
            serialized_managers = UserSerializer(all_managers, many=True)
            return Response({"managers": serialized_managers.data})
        else:
            return Response({"message": "You Are Not Authorized"},status = status.HTTP_403_FORBIDDEN)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            username = request.data['username']
            if username:   
                user = get_object_or_404(User, username=username)
                managers = Group.objects.get(name="Manager")
                managers.user_set.add(user)

                serialized_User = UserSerializer(user)
                return Response({"message": "User role changed to manager", "data":serialized_User.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Provide a valid username"}, status = status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"message": "You Are Not Authorized"},status = status.HTTP_403_FORBIDDEN)



class ManagerSingleAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def delete(request, userId):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            selected_User = get_object_or_404(User, id=userId)
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(selected_User)
            return Response({"message" : "user has been removed from manger's group"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You Are Not Authorized"}, status=status.HTTP_403_FORBIDDEN)
    



class ManagerDeliveryCrewListAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            deliveryCrewsGroup = Group.objects.get(name='Delivery crew')
            allDeliveryCrews = User.objects.filter(groups=deliveryCrewsGroup)
            serializedDeliveryCrews = UserSerializer(allDeliveryCrews, many=True)
            return Response(serializedDeliveryCrews.data)
        else:
            return Response({"message": "You Are Not Authorized"},status = status.HTTP_403_FORBIDDEN)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            username = request.data['username']
            if username:
                user = get_object_or_404(User, username=username)
                deliveryCrewsGroup = Group.objects.get(name='Delivery crew')
                deliveryCrewsGroup.user_set.add(user)

                serialized_User = UserSerializer(user)
                return Response({"message": "User added to the Delivery crew group", "user": serialized_User.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Provide a valid username"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "You Are Not Authorized"}, status=status.HTTP_403_FORBIDDEN)

        
        


class ManagerDeliveryCrewSingleAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request, userId):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            selected_user = get_object_or_404(User, id=userId)
            serializedDeliveryCrews = UserSerializer(selected_user)
            return Response(serializedDeliveryCrews.data)
        else:
            return Response({"message": "You Are Not Authorized"},status = status.HTTP_403_FORBIDDEN)

    @permission_classes([IsAuthenticated])
    def delete(self, request, userId):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            selected_User = get_object_or_404(User, id=userId)
            deliveryCrewsGroup = Group.objects.get(name='Delivery crew')

            if deliveryCrewsGroup.user_set.filter(id=userId).exists():
                deliveryCrewsGroup.user_set.remove(selected_User)
                return Response({"message": "User removed from Delivery crew group"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User does not exist in the Delivery crew group"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    


class CartMenuItemsListAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        token_header = request.headers.get('Authorization')
        if token_header:
            token_key = token_header.split(' ')[1]
            token = Token.objects.get(key=token_key)
            user_id = token.user_id
            userCart = Cart.objects.filter(user=user_id)
            serialized_cart = CartSerializer(userCart, many=True)
            return Response(serialized_cart.data)
        else:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        

    @permission_classes([IsAuthenticated])
    def post(self, request):
        token_header = request.headers.get('Authorization')
        if token_header:
            token_key = request.headers.get('Authorization').split(' ')[1]
            token = Token.objects.get(key=token_key)
            user_id = token.user_id
            selected_User = get_object_or_404(User, id=user_id)

            menuItemId = request.data.get('menuitem')
            selected_menuItem = get_object_or_404(MenuItem, id=int(menuItemId))
            received_quantity = int(request.data.get('quantity', 1))  # Default quantity to 1 if not provided
            
            received_unit_price = float(selected_menuItem.price)
            received_price = float(received_unit_price) * float(received_quantity)

            cart = Cart(
                user=selected_User,
                menuitem=selected_menuItem,
                quantity=received_quantity,
                unit_price=received_unit_price,
                price=received_price
            )
            cart.save()

            serialized_cart = CartSerializer(cart)
            return Response(serialized_cart.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    @permission_classes([IsAuthenticated])
    def delete(self, request):
        token_header = request.headers.get('Authorization')
        if token_header:
            token_key = request.headers.get('Authorization').split(' ')[1]
            token = Token.objects.get(key=token_key)
            user_id = token.user_id
            selected_User = get_object_or_404(User, id=user_id)
            cart_MenuItems = Cart.objects.filter(user=selected_User)
            cart_MenuItems.delete()
            return Response({"message": "Cart deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        

@permission_classes([IsAuthenticated])
class ordersListAPIView(APIView):
    def get(self, request):
        if request.user.groups.filter(name="Delivery crew").exists():
            all_Orders = Order.objects.exclude(delivery_crew__isnull=True)
            ordering = request.query_params.get('ordering')
            perpage = request.query_params.get('perpage', default=2)
            page = request.query_params.get('page', default=1)

            if ordering:
                all_Orders = all_Orders.order_by(ordering)

            paginator = Paginator(all_Orders, per_page = perpage)
            try:
                all_Orders = paginator.page(number = page)
            except EmptyPage:
                all_Orders = []
            serialized_Order = OrderSerializer(all_Orders, many=True)
            return Response({"order": serialized_Order.data}, status=status.HTTP_200_OK)

        if not request.user.groups.filter(name="Manager").exists():
            token_key = request.headers.get('Authorization').split(' ')[1]
            token = Token.objects.get(key=token_key)
            user_id = token.user_id
            selected_User = get_object_or_404(User, id=user_id)

            all_Orders = Order.objects.filter(user=selected_User)
            all_OrderItems = OrderItem.objects.filter(order=selected_User)
            serialized_orderItems = OrderItemSerializer(all_OrderItems, many=True)
            serialized_Order = OrderSerializer(all_Orders, many=True)
            return Response({"order": serialized_Order.data}, status=status.HTTP_200_OK)
        
        if request.user.groups.filter(name="Manager").exists():
            all_Orders = Order.objects.all()
            serialized_Order = OrderSerializer(all_Orders, many=True)
            return Response(serialized_Order.data, status=status.HTTP_200_OK)
        
    
    def post(self, request):
        if not request.user.groups.filter(name="Manager").exists():
            token_key = request.headers.get('Authorization').split(' ')[1]
            token = Token.objects.get(key=token_key)
            user_id = token.user_id
            selected_User = get_object_or_404(User, id=user_id)

            total_orderPrice = Cart.objects.filter(user=selected_User).aggregate(total_orderPrice=Sum('price'))['total_orderPrice']

            order = Order.objects.create(user=selected_User, total=total_orderPrice, date=date.today())

            user_cart = Cart.objects.filter(user=selected_User)

            for cart in user_cart:
                new_orderItem = OrderItem()
                new_orderItem.order = selected_User
                new_orderItem.menuitem = cart.menuitem
                new_orderItem.quantity = cart.quantity
                new_orderItem.unit_price = cart.unit_price
                new_orderItem.price = cart.price
                new_orderItem.save()

            user_cart.delete()  # Delete all items from the cart for this user

            return Response({"message": "Items added to the cart"}, status=status.HTTP_200_OK)     


class ordersSingleAPIView(APIView):
    def get(self, request, orderId):
        if not request.user.groups.filter(name="Manager").exists():
            token_key = request.headers.get('Authorization').split(' ')[1]
            token = Token.objects.get(key=token_key)
            user_id = token.user_id
            selected_User = get_object_or_404(User, id=user_id)
            
            if Order.objects.filter(id=orderId, user=selected_User).exists():
                all_orderItems = OrderItem.objects.filter(order=selected_User)
                serialized_orderItems = OrderItemSerializer(all_orderItems, many=True)
                return Response(serialized_orderItems.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
        if request.user.groups.filter(name="Manager").exists():
            all_orders = OrderItem.objects.all()
            serialized_order = OrderItemSerializer(all_orders, many=True)
            return Response(serialized_order.data, status=status.HTTP_200_OK)
        
        if request.user.groups.filter(name="Delivery crew").exists():
            all_orderItems = OrderItem.objects.filter(order_set__delivery_crew=True)
            serialized_orderItems = OrderItemSerializer(all_orderItems, many=True)
            return Response(serialized_orderItems.data, status=status.HTTP_200_OK)


    @permission_classes([IsAuthenticated])
    def patch(self, request, orderId):
        if request.user.groups.filter(name="Delivery crew").exists():
            order_status = request.POST.get('order_status')
            selected_order = get_object_or_404(Order, id=orderId)
            selected_order.status = order_status
            selected_order.save()

            serialized_Order = OrderSerializer(selected_order)
            return Response({"message": "Order Status changed", "details": serialized_Order.data}, status=status.HTTP_200_OK)
        
        elif request.user.groups.filter(name="Manager").exists():
            selected_order = get_object_or_404(Order, id=orderId)
            serialized_Order = OrderSerializer(selected_order, data=request.data, partial=True)
            if serialized_Order.is_valid():
                serialized_Order.save()
                return Response(serialized_Order.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized_Order.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


    @permission_classes([IsAuthenticated]) 
    def put(self, request, orderId):
        if request.user.groups.filter(name="Manager").exists():
            selected_order = get_object_or_404(Order, id=orderId)
            serialized_Order = OrderSerializer(selected_order, data=request.data)
            if serialized_Order.is_valid():
                serialized_Order.save()
                return Response(serialized_Order.data, status=status.HTTP_200_OK)
            else:
                return Response(serialized_Order.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        

    @permission_classes([IsAuthenticated])
    def delete(self, request, orderId):
        if request.user.groups.filter(name="Manager").exists():
            selected_order = get_object_or_404(Order, id=orderId)
            selected_order.delete()
            return Response({"message": "Order Deleted"}, status=status.HTTP_200_OK)

