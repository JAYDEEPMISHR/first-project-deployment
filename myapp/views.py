from django.shortcuts import render,redirect
from .models import User
from django.conf import settings
from django.core.mail import send_mail
import random


# Create your views here.

def index(request):
	return render(request,'index.html')

def seller_index(request):
	return render(request,'seller-index.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
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
					return render(request,'seller-index.html')
				else:
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return render(request,'index.html')
			else:
				msg="Invalid password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="Email Not registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_pic']
		del request.session['mobile']
		return render(request,'index.html')
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
			return render(request,'change-password.html',{'msg':msg})
	else:
		return render(request,'change-password.html')

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
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
		return render(request,'change-password.html')

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
		return render(request,'profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'profile.html',{'user':user})


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

def mobile_login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(mobile=request.POST['mobile'])
			if user.password==request.POST['password']:
				request.session['mobile']=user.mobile
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				return render(request,'index.html')
			else:
				msg="Invalid password"
				return render(request,'mobile-login.html',{'msg':msg})
		except:
			msg="Mobile Number is not registered"
			return render(request,'mobile-login.html',{'msg':msg})
	else:
		return render(request,'mobile-login.html')