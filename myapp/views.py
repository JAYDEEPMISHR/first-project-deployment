from django.shortcuts import render,redirect
from .models import User
# Create your views here.

def index(request):
	return render(request,'index.html')

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
						profile_pic=request.FILE['profile_pic']
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
		return render(request,'login.html')
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

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		user.city=request.POST['city']
		user.zipcode=request.POST['zipcode']
		user.save()
		msg="Profile Updated successfully"
		return render(request,'profile.html',{'user':user,'msg':msg})
	else:
		return render(request,'profile.html',{'user':user})


