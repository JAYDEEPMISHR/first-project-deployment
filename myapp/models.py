from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	city=models.CharField(max_length=100)
	zipcode=models.PositiveIntegerField()
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to="profile_pic/",default="")
	usertype=models.CharField(max_length=100, default="buyer")

	def __str__(self):
		return self.fname+' '+self.lname

class Product(models.Model):
	categories=(
			("Mobile","Mobile"),
			("Camera","Camera"),
			("Laptop","Laptop"),
			("Head-phone","Head-phone")
		)
	product_categories=models.CharField(max_length=100,choices=categories)
	product_name=models.CharField(max_length=100)
	product_price=models.PositiveIntegerField()
	product_desc=models.TextField()
	product_pic=models.ImageField(upload_to="product_pic/",default="")

	def __str__(self):
		return self.product_name+'--'+self.product_categories