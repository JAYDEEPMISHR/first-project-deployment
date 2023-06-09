from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import random
import json
from django.utils import timezone
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'




# Create your views here.

def validate_email(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}

	return JsonResponse(data)

def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="seller":
			return redirect('seller-index')
		else:
			products=Product.objects.all()
			carts=Cart.objects.filter(user=user,payment_status=False)
			return render(request,'index.html',{'products':products,'carts':carts})
	except:
		products=Product.objects.all()
		return render(request,'index.html',{'products':products})

def seller_index(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-index.html')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg="Email is already registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:

				user=User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						city=request.POST['city'],
						zipcode=request.POST['zipcode'],
						password=request.POST['password'],
						profile_pic=request.FILES['profile_pic'],
						usertype=request.POST['usertype']
					)
				msg="User SignUP successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password & Confirm Password does not match"
				return render(request,'signup.html')
	else:	
	 	return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="seller":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					request.session['usertype']=user.usertype
					return redirect("seller-index")	
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					request.session['usertype']=user.usertype
					wishlists=Wishlist.objects.filter(user=user)
					request.session['wishlist_count']=len(wishlists)
					carts=Cart.objects.filter(user=user,payment_status=False)
					request.session['cart_count']=len(carts)
					return redirect('index')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email not registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')


def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_pic']
		del request.session['wishlist_count']
		del request.session['cart_count']
		return redirect('index')
	except:
		return render(request,'login.html')

def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				return redirect('logout')
			else:
				msg="New Password and Confirm New Password does not match"
				return render(request,'change-password.html',{'msg':msg})
		else:
			msg="Old Password does not matched"
			carts=Cart.objects.filter(user=user,payment_status=False)
			return render(request,'change-password.html',{'msg':msg,'carts':carts})
	else:
		#user=User.objects.get(email=request.session['email'])
		#carts=Cart.objects.get(user=user)
		return render(request,'change-password.html')


def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="seller":
			if user.password==request.POST['old_password']:
				if request.POST['new_password']==request.POST['cnew_password']:
					user.password=request.POST['new_password']
					user.save()
					return redirect('logout')
				else:
					msg="New Password and Confirm New Password does not match"
					return render(request,'seller-change-password.html',{'msg':msg})
			else:
				msg="Old Password does not matched"
				return render(request,'seller-change-password.html',{'msg':msg})
		else:
			return render(request,'seller-change-password.html',{'msg':msg})
	else:
		return render(request,'seller-change-password.html')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.city=request.POST['city']
		user.zipcode=request.POST['zipcode']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Profile Updated successfully"
		request.session['profile_pic']=user.profile_pic.url
		carts=Cart.objects.filter(user=user,payment_status=False)
		return render(request,'profile.html',{'user':user,'msg':msg,'carts':carts})
	else:
		carts=Cart.objects.filter(user=user,payment_status=False)
		return render(request,'profile.html',{'user':user,'carts':carts})

def seller_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.city=request.POST['city']
		user.zipcode=request.POST['zipcode']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Profile Updated successfully"
		request.session['profile_pic']=user.profile_pic.url
		return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'seller-profile.html',{'user':user})


def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OTP for Forgot Password'
			message = 'Hello ' + user.fname + ', Your OTP for forgot password is: '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,]
			send_mail( subject, message, email_from, recipient_list)
			return render(request,'otp.html',{'email':user.email,'otp':otp})

		except:
			msg="Email not registered"
			return render(request,'forgot-password.html',{'msg':msg})

	else:
		return render(request,'forgot-password.html')

def verify_otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'New-Password.html',{'email':email})
	else:
		msg="OTP is Invalid"
		return render(request,'otp.html',{'email':email,'otp':otp,'msg':msg})

def New_password(request):
	email=request.POST['email']
	np=request.POST['New-Password']
	cnp=request.POST['cNew-Password']
	if np==cnp:
		user=User.objects.get(email=email)
		user.password=np
		user.save()
		msg="Password Updated successfully"
		return render(request,'login.html',{'msg':msg})

	else:	
		msg="New-Password and Confirm New-Password does not matched"
		return render(request,'New-Password.html',{'msg':msg})

def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
					seller=seller,
					product_category=request.POST['product_category'],
					product_name=request.POST['product_name'],
					product_price=request.POST['product_price'],
					product_desc=request.POST['product_desc'],
					product_image=request.FILES['product_image'],
					product_stock=request.POST['product_stock'],
			)
		msg="Product added successfully"
		return render(request,'seller-add-product.html',{'msg':msg})
	else:
		return render(request,'seller-add-product.html')

def seller_view_product(request):
	user=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=user)
	return render(request,'seller-view-product.html',{'products':products})

def seller_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller-product-detail.html',{'product':product})

def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_category=request.POST['product_category']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.POST['product_image']
		except:
			pass
		product.product_stock=request.POST['product_stock']
		product.save()
		return redirect('seller-view-product')
	else:
		return render(request,'seller-edit-detail.html',{'product':product})

def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')

def product_detail(request,pk):
	wishlist_flag=False
	cart_flag=False
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	try:
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass

	try:
		Cart.objects.get(user=user,product=product)
		cart_flag=True
	except:
		pass
	carts=Cart.objects.filter(user=user)
	return render(request,'product-detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag,'carts':carts})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(
		product=product,
		user=user
		)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	carts=Cart.objects.filter(user=user,payment_status=False)
	return render(request,'wishlist.html',{'wishlists':wishlists,'carts':carts})

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		product=product,
		user=user,
		product_price=product.product_price,
		product_qty=1,
		total_price=product.product_price,
		payment_status=False
		)
	product.cart_status=True
	product.save()
	return redirect('cart')

def cart(request):
	net_price=0
	total_qty=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	for i in carts:
		net_price=net_price+i.total_price
		total_qty=total_qty+i.product_qty
	return render(request,'cart.html',{'carts':carts,'net_price':net_price,'total_qty':total_qty})

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	product.cart_status=False
	product.save()
	return redirect('cart')

def change_qty(request):
	cart_id=int(request.POST['cart_id'])
	product_qty=int(request.POST['product_qty'])
	cart=Cart.objects.get(pk=cart_id)
	cart.product_qty=product_qty
	cart.total_price=product_qty*cart.product_price
	cart.save()
	return redirect('cart')

def mobile(request):
	
	products=Product.objects.filter(product_category="Mobile")
	return render(request,'index.html',{'products':products})

def accesories(request):
	products=Product.objects.filter(product_category="Accessories")
	return render(request,'index.html',{'products':products})

def camera(request):
	products=Product.objects.filter(product_category="Camera")
	return render(request,'index.html',{'products':products})

def seller_mobile(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Mobile")
	return render(request,"seller-index.html",{'products':products,'seller':seller})

def seller_accessories(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Accessories")
	return render(request,"seller-index.html",{'products':products,'seller':seller})

def seller_cameras(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller,product_category="Camera")
	return render(request,"seller-index.html",{'products':products,'seller':seller})

def checkout(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	net_price=0
	for i in carts:
		net_price=net_price+i.total_price
	return render(request,'checkout.html',{'user':user,'carts':carts,'net_price':net_price})

@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100

	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
		}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html')
	return JsonResponse({'id': session.id})

def success(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user, payment_status=False)
	for i in carts:
		i.payment_status=True
		i.ordered_date=timezone.now()
		i.save()
		product=Product.objects.get(id=i.product.id)
		product.cart_status=False
		product.save()
	carts=Cart.objects.filter(user=user, payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user, payment_status=True)
	return render(request,'myorder.html',{'carts':carts})

def seller_order(request):
	seller=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(payment_status=True)
	orders=[]
	for i in carts:
		if i.product.seller==seller:
			orders.append(i)
	return render(request,'seller-order.html',{'orders':orders})
