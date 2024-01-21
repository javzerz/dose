from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, EditProfileForm, UpdateProfileForm
from core.models import Category, Product, UserProfile, NutritionFacts
from django.contrib.staticfiles import finders
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.views.generic import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserChangeForm
from .cart import Cart
from django.urls import reverse
from django.db.models import Q, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import json
import os

def index(request):
	products = Product.objects.filter(is_sold = False)
	categories = Category.objects.all()

	return render(request,'core/homepage.html', {
		'categories': categories,
		'products': products,
		})

def contact(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    volume = cart.cart_total_volume()
    total_quantity = sum(quantities.values())
    percent_bag = {key: f"{value / total_quantity * 100:.2f}%" for key, value in quantities.items()} if total_quantity != 0 else {}

    return render(request, 'core/shop.html', {"cart_products": cart_products, "cart": cart, 
        "quantities": quantities, "volume": volume, "totals": totals, "percent_bag": percent_bag})


def item(request):
    categories = Category.objects.all().prefetch_related('products')
    
    root = {
        'name': 'BUY THESE',  # Set a root name
        'children': []
    }

    for category in categories:
        category_info = {
            'name': category.name,
            'children': [
                {
                    'name': product.name,
                    'url': reverse('detail', kwargs={'pk': product.pk})  # Generate the product URL
                }
                for product in category.products.all()
            ]
        }
        root['children'].append(category_info)
    
    file_path = os.path.join(settings.STATIC_ROOT, 'item.json')
    with open(file_path, 'w') as json_file:
        json.dump(root, json_file, indent=4)
    
    return JsonResponse(root, safe=False)
	
def detail(request, pk):
	products = get_object_or_404(Product, pk=pk)
	return render(request, 'core/detail.html',{'products':products})

def store(request):
    products = Product.objects.filter(is_sold = False)
    cart = Cart(request)
    nutrition_facts = NutritionFacts.objects.all()
    total_nutrition = calculate_total_nutrition(cart)
    categories = Category.objects.all()
    cart_products = cart.get_products()
    quantities = cart.get_quants()
    total_quantity = sum(quantities.values())
    percent_bag = {key: f"{value / total_quantity * 100:.2f}%" for key, value in quantities.items()} if total_quantity != 0 else {}

    return render(request,'core/store.html', {
        'categories': categories,
        'products': products,
        'total_nutrition':total_nutrition,
        "nutrition_facts": nutrition_facts,
        "cart_products":cart_products, 
        "quantities":quantities,
        'total_quantity':total_quantity,
        "percent_bag":percent_bag,
        })

def product_list(request):
    products = Product.objects.filter(is_sold = False)
    categories = Category.objects.all()

    return render(request,'core/product_list.html', {
        'categories': categories,
        'products': products,
        })

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "core/cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('products_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=product_qty)
        
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_add_or_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('products_id'))
        product_qty = int(request.POST.get('product_qty'))

        if cart.is_product_in_cart(product_id):
            cart.update(product=product_id, quantity=product_qty)
        else:
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_add_or_update_multiple(request):
    cart = Cart(request)
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('product_id_'):
                index = key.split('_')[-1]
                product_id = int(request.POST.get(f'product_id_{index}'))
                product_qty = int(request.POST.get(f'product_qty_{index}', 1))

                if cart.is_product_in_cart(product_id):
                    cart.update(product=product_id, quantity=product_qty)
                else:
                    product = get_object_or_404(Product, id=product_id)
                    cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id,quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        return response

# def email_check(user):
#     return user.email.startswith('javier')
def calculate_nutrition(request):
    cart = Cart(request)
    cart_products = cart.get_products()

    # Extract the product IDs from the cart products
    selected_product_ids = [product.id for product in cart_products]

    # Query the related nutrition facts
    nutrition_facts = NutritionFacts.objects.filter(product__id__in=selected_product_ids)

    # pull total nut
    total_nutrition = calculate_total_nutrition(cart)

    # Additional context data, like totals and quantities, can be passed to the template as well
    context = {
        'total_nutrition': total_nutrition,
        'totals': cart.cart_total(),
        'quantities': cart.get_quants(),
    }

    return render(request, 'core/nutrition.html', context)


def calculate_total_nutrition(cart):
    cart_products = cart.get_products()
    selected_product_ids = [product.id for product in cart_products]
    nutrition_facts = NutritionFacts.objects.filter(product__id__in=selected_product_ids)

    # Calculate the sums
    total_nutrition = {
        'calories': sum(nf.calories for nf in nutrition_facts if nf.calories),
        'total_fat': sum(nf.total_fat for nf in nutrition_facts if nf.total_fat),
        'cholesterol': sum(nf.cholesterol for nf in nutrition_facts if nf.cholesterol),
        'dietary_fiber': sum(nf.dietary_fiber for nf in nutrition_facts if nf.dietary_fiber),
        'sugar': sum(nf.sugar for nf in nutrition_facts if nf.sugar),
        'protein': sum(nf.protein for nf in nutrition_facts if nf.protein),
    }

    return total_nutrition



class UserFormView(View):
    form_class = UserForm
    template_name = 'core/registration.html'

    #display form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #add user
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile')

        return render(request, self.template_name, {'form': form})

@login_required
def profile(request):
    args = {'user': request.user}
    return render(request, 'core/profile.html', args)

@login_required
def edit_profile(request):

    if request.method == 'POST':
        form1 = EditProfileForm(request.POST,instance=request.user)
        form2 = UpdateProfileForm(request.POST,instance=request.user.userprofile)

        if form1.is_valid() and form2.is_valid():
            username = form1.cleaned_data['username']
            email = form1.cleaned_data['email']
            phone = form2.cleaned_data['phone']
            form1.save()
            form2.save()
            return redirect('/profile')

        else:
            return redirect('/profile/edit')

    else:
        form1 = EditProfileForm(instance=request.user)
        form2 = UpdateProfileForm(instance=request.user.userprofile)
        args = {'form1': form1,'form2': form2 }
        return render(request, 'core/edit_profile.html', args)




