from django.urls import path
from . import views
from .forms import *

urlpatterns = [
   path('', views.index, name="index"),
   path('products/', views.products, name="products"),
   path('products/<int:prodid>/', views.product_individual, name="individual_product" ),
   path('register/', views.UserSignupView.as_view(), name="register"),
   path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
   path('logout/', views.logout_user, name="logout"),
   path('addbasket/<int:prodid>/', views.add_to_basket, name="add_basket"),
   path('basket/', views.show_basket, name="show_basket"),
   path('removeitem/<int:sbi>', views.remove_item, name="remove_basket"),
   path('additem/<int:sbi>', views.add_item, name="add_basket"),
   path('order/', views.order, name='order'),
   path('orderhistory/', views.previous_orders, name="order_history")
] 