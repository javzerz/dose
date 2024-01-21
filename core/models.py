from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.timesince import timesince
from colorfield.fields import ColorField
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username

class Category(models.Model):
	name = models.CharField(max_length=255)

	class Meta:
		ordering = ('name',)
		verbose_name_plural = "Categories"

	#show name of categories
	def __str__(self):
		return self.name

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True,null=True)
	benefits = models.TextField(blank=True,null=True)
	serving_info = models.TextField(blank=True,null=True)
	price = models.FloatField()
	servings = models.FloatField(blank=True,null=True)
	image = models.ImageField(upload_to='products_images', blank=True,null=True)
	is_sold = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
	color = ColorField(default='#FF0000')

	class Meta:
		ordering = ('name',)
		verbose_name_plural = "Products"

	def __str__(self):
		return self.name

class NutritionFacts(models.Model):
	product = models.ForeignKey(Product, related_name='NutritionFacts', on_delete=models.CASCADE)
	calories = models.FloatField(blank=True,null=True)
	total_fat = models.FloatField(blank=True,null=True)
	cholesterol = models.FloatField(blank=True,null=True)
	dietary_fiber = models.FloatField(blank=True,null=True)
	sugar = models.FloatField(blank=True,null=True)
	protein = models.FloatField(blank=True,null=True)

	class Meta:
		verbose_name_plural = "NutritionFacts"

	def __str__(self):
		return self.product.name


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)