from django.db import models


class Owner(models.Model):
	name = models.CharField(max_length=64)
	email = models.EmailField()
	# Hashed password 
	password = models.CharField(max_length=128)
	contact_info = models.TextField(max_length=256)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=32)
	
	def __str__(self):
		return self.name


class Item(models.Model):
	owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.PROTECT)
	name = models.CharField(max_length=64)
	description = models.TextField(max_length=512)
	available_date = models.DateField()
	price = models.CharField(max_length=64)

	def __str__(self):
		return "'{}' in category {} posted by {}".format(self.name, self.category.name, self.owner.name)


