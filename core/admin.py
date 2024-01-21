from django.contrib import admin

# Register your models here.
from .models import Category, Product, UserProfile, NutritionFacts

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['user']
#     search_fields = ['user']

admin.site.register(Category)
admin.site.register(NutritionFacts)
admin.site.register(Product) 
admin.site.register(UserProfile)
# admin.site.register(UserProfileAdmin)