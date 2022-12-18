from email import message
from operator import imod
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from products.models import Product

# Create your views here.


def signin(request):
    logged = True
    if request.method == 'POST' and 'btn' in request.POST:
        username=request.POST['user']
        password =request.POST['password']
        user=auth.authenticate(username = username , password = password)
        print('h')
        if user is not None :
            if 'remember' not in request.POST:

                request.session.set_expiry(0)

            auth.login(request, user )
            logged = True
            print("1")


        else:
            pass
            print("33")


        return redirect('signin')



    else:
        return render(request,'accounts/signin.html',context={
            'logged':logged
        } )

def signup(request):
    is_added=False
    if request.method =='POST' and 'btn' in request.POST:
        fname=None
        lname=None
        address=None
        address2=None
        city=None
        state=None
        zip=None
        email=None
        username=None
        password=None
        agree=None
        
        print("1")
        fname=request.POST['fname']
        lname=request.POST['lname']
        address=request.POST['address']
        address2=request.POST['address2']
        city=request.POST['city']
        state=request.POST['state']
        zip=request.POST['zip']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        agree=request.POST['agree']
        print("2")

        if fname and lname and address and address2 and city and state and zip and email and username and password :
            
            
            if agree =='on':
                user= User.objects.create_user(first_name=fname, last_name =lname, email=email, username=username,password=password)
                user.save()
                
                print("x")
                userp = UserProfile(user=user,address=address,address2=address2,city=city,state=state,zip_number=zip)
                userp.save()
                is_added=True
                print("3")


    return render(request,'accounts/signup.html',{
        'is_added' :is_added
    })


def logout(request):
    if request.user.is_authenticated :
        auth.logout(request)

    return redirect('index')
    

    
    

def profile(request):
    
    if 'save' in request.POST and request.method=='POST':
        userp = UserProfile.objects.get(user = request.user)
        if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['zip'] and request.POST['city'] and request.POST['state'] and request.POST['email'] and request.POST['username'] and request.POST['password']:
            
            request.user.first_name = request.POST['fname']
            request.user.last_name = request.POST['lname']
            userp.address = request.POST['address']
            userp.address2 = request.POST['address2']
            request.user.email = request.POST['email']
            request.user.username = request.POST['username']
            if not request.POST['password'].startswith('pbkdf2_sha256$'):

                request.user.set_password(request.POST['password'])

            userp.city = request.POST['city']
            userp.state = request.POST['state']
            userp.zip_number = request.POST['zip']

            request.user.save()
            userp.save()
            # auth.logout(request)
            print(1)
            return redirect('profile')
            
    else:
        if request.user.is_anonymous:
            # return redirect('index')
            return render(request,'accounts/profile.html')


        if request.user is not None :
            
            userp = UserProfile.objects.get(user = request.user)
            context={
                'fname':request.user.first_name,
                'lname':request.user.last_name,
                'email':request.user.email,
                'user':request.user.username,
                'password':request.user.password,
                'address':userp.address,
                'address2':userp.address2,
                'city':userp.city,
                'zip':userp.zip_number,
                'state':userp.state,
            }
            return render(request,'accounts/profile.html', context)
        else:
            return redirect('profile')
 


def favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,fav=pro_fav).exists():
            print(1)

        else :
            user_profile= UserProfile.objects.get(user = request.user)
            user_profile.fav.add(pro_fav)
            print(2)

        return redirect('/products/' + str(pro_id))
    else:
        return redirect('index')


def show_fav(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        user_profile= UserProfile.objects.get(user = request.user)
        pro= user_profile.fav.all()

        context={
            'product':pro
        }
        return render(request,'products/products.html', context)