
from django.contrib import admin
from django.urls import path, include
from core import views
from core.views import index, store, contact, detail, product_list, cart_summary, profile, calculate_nutrition
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView
from django.views.generic import ListView, DetailView
from core.forms import CustomAuthForm

app_name = 'dose'

urlpatterns = [
    path('', index, name='homepage'), #homepage
    path('item/', views.item, name='item'), #json testing
    path('shop/', contact, name='shop'), 
    path('store/', store, name='store'), 
    path('nutrition/', calculate_nutrition, name='nutrition'),
    path('product_list/', product_list, name='product_list'), #placeholder
    path('product_list/<int:pk>/', views.detail, name='detail'), #detailviews
    path('cart/',views.cart_summary,name='cart_summary'),
    path('cart/add/',views.cart_add,name='cart_add'),
    path('cart/add_or_update/',views.cart_add_or_update,name='cart_add_or_update'),
    path('cart/add_or_update_multiple/',views.cart_add_or_update_multiple,name='cart_add_or_update_multiple'),
    path('cart/delete/',views.cart_delete,name='cart_delete'),
    path('cart/update/',views.cart_update,name='cart_update'),
    path('admin/', admin.site.urls),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=CustomAuthForm), name='login'),
    path('registration/', views.UserFormView.as_view(), name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
]

