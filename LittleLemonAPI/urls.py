from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
urlpatterns =[
    path('menu-items', views.MenuItemListAPIView.as_view()),
    path('menu-items/<int:menuItem>', views.MenuItemSingleAPIView.as_view()),
    path('category', views.CategoryListAPIView.as_view()),
    path('category/<int:categoryId>', views.CategorySingleAPIView.as_view()),
    path('groups/manager/users', views.ManagerListAPIView.as_view()),
    path('groups/manager/users/<int:userId>', views.ManagerSingleAPIView.as_view()),
    path('groups/delivery-crew/users', views.ManagerDeliveryCrewListAPIView.as_view()),
    path('groups/delivery-crew/users/<int:userId>', views.ManagerDeliveryCrewSingleAPIView.as_view()),
    path('cart/menu-items', views.CartMenuItemsListAPIView.as_view()),
    path('orders', views.ordersListAPIView.as_view()),
    path('orders/<int:orderId>', views.ordersSingleAPIView.as_view()),
]