from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import UserSignupForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import *
from .forms import OrderForm

class UserSignupView(CreateView):  #user registration form and template render
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()          #log in user after successful
        login(self.request, user)
        return redirect('/')
    
def index(request):
    return render(request, 'index.html') #homepage

def products(request):
    products = Product.objects.all()    #all products display page NOT INDIVIDUAL
    return render(request, 'all_products.html', {'products':products})

def product_individual(request, prodid):
    product = Product.objects.get(id=prodid)        #individual product fetch from db
    return render(request, 'product.html', {'product':product})

class UserLoginView(LoginView):     #render template for the user to login
    template_name='login.html'

def logout_user(request):
    logout(request)         #redirect to home after logout
    return redirect("/")

def open_view(request):
    return render(request, 'index.html')

@login_required
def locked_view(request):
    return render(request, 'index.html')    #log in required to access pages/excl home page

@login_required
def add_to_basket(request, prodid):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:      #create basket if there is no existing basket
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    product = Product.objects.get(id=prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id = product).first()
    if sbi is None:
        sbi = BasketItem(basket_id=basket, product_id = product)
        sbi.save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return redirect("/products")    #redirect to all products page

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return render(request, 'basket.html', {'empty':True})
    else:
        sbi = BasketItem.objects.filter(basket_id=basket)
        if sbi.exists():
            return render(request, 'basket.html', {'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'basket.html', {'empty':True})
        
@login_required
def remove_item(request,sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect("/basket")
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity-1
            basketitem.save()
        else:
            basketitem.delete()
    return redirect("/basket")

@login_required
def add_item(request, sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect("/basket")
    else:
        basketitem.quantity += 1
        basketitem.save()
    return redirect("/basket")

@login_required
def order(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return redirect("/")
    sbi = BasketItem.objects.filter(basket_id=basket)
    if not sbi.exists():
        return redirect("/")
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.basket_id = basket
            total = 0.0
            for item in sbi:
                total += float(item.item_price())
            order.total_price = total
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order':order, 'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})
    else:
        form = OrderForm()
        return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})

@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html', {'orders':orders})