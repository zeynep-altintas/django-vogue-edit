from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Order)