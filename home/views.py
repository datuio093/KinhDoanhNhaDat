from base64 import urlsafe_b64decode
from email import message
# from email.message import EmailMessage
from gzip import FNAME
# from lib2to3.pgen2.tokenize import generate_tokens
from multiprocessing import context
import re
from tkinter.messagebox import NO
from turtle import title
from unittest.result import failfast
from chothuenha import settings
from django.shortcuts import render, redirect , reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_tokens
from .models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import json
from django.shortcuts import get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

def get_home(request):
    post = HomeMypost.objects.order_by('-pk')
    review  = Review.objects.order_by('-pk')

    if request.method == "POST":
        city = request.POST.get('city')
        district = request.POST.get('district')
        address = request.POST.get('ward')

        post = HomeMypost.objects.all()

        try:
            if city:
                _, city = city.split('-')
                post = post.filter(city=city)
            if district:
                _, district = district.split('-')
                post = post.filter(district=district)
            if address:
                _, address = address.split('-')
                post = post.filter(address=address)
        except ValueError:
            pass

        return render(request, 'index.html', {'post': post, 'review': review})
        

    return render(request, 'index.html', {'post':post , 'review':review})



def get_login(request):
    #redirect to home when user signin
    if request.user.is_authenticated:
        return redirect('home')   
    
    if request.method == "POST":
        username = request.POST['User']
        password1 = request.POST['Password']

        users = authenticate(username=username, password = password1)

        # if users.is_active == False:
        #     messages.error(request, "You Must Be Confirm Email Before Login")
        #     return redirect('login')
 

        if users is not None:
            login(request,users)
            

            return get_home(request)
            
        else:
            messages.error(request, "Login Fail")   
            
          
            
    return render(request , 'login.html')

def get_register(request):
    if request.user.is_authenticated:
          return get_home(request)

    if request.method == "POST":
        email = request.POST['Email']
        username = request.POST['User']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['Password1']
        pass2 = request.POST['Password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist")
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, "Email already exist")
            return redirect('register')
        
        if pass1 != pass2:
            messages.error(request, "Password didn't match")
            return redirect('register')

        if not username.isalnum():
             messages.error(request, "Username must be Alpha-Numberic !")
             return redirect('register')

       
        myuser = User.objects.create_user(username , email , pass1 )
        myuser.first_name = fname
        myuser.last_name = lname
    
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been successfully created")

       # Welcome email

        # subject = "Welcome to Django"
        # message = "Hello " + myuser.first_name + myuser.last_name
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject , message ,from_email , to_list, fail_silently=True)

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email Django"
        message2 = render_to_string('email_confirmation.html',{
            'fname' : myuser.first_name,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token' : generate_tokens.make_token(myuser)
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],

        )
        email.fail_silently = True
        email.send()
        return redirect('login')
    
    return render(request , 'register.html')


def get_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError , User.DoesNotExist ):
        myuser : None

    if myuser is not None and generate_tokens.check_token(myuser , token):
        myuser.is_active = True
        myuser.save()
        login(request , myuser) 
        return redirect('home')
    else:
        return redirect(request, 'activation_fail.html')

def logout_user(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('login')

def get_all_properties(request):
 
    post = HomeMypost.objects.order_by('-pk')
    return render(request, 'properties.html', {'post':post})


def post(request):
    if request.user.is_authenticated == False:
        return redirect('login') 
    # create post 
    if request.method == "POST":
        
        
        # username = request.POST['username']
        title = request.POST['tieude']
    
        descrip = request.POST['mota']
        v1,address = request.POST['address'].split('-') #phuong xa
        v1,city = request.POST['city'].split('-')  #thanh pho
        v1,district =  request.POST['district'].split('-')  #quan

        addressdetail = request.POST['addressdetail']
        mattien = request.POST['mattien']
        
        price = request.POST['price']

        chieudai = request.POST['cd']
        chieurong = request.POST['cr']
        dientich = request.POST['dt']

        name = request.POST['name']
        email = request.POST['email']


        bedroom = request.POST['bedroom']
        bathroom = request.POST['bathroom']
        solau = request.POST['solau']

        images = request.FILES.get('images')

        

        #save post to db
        post = HomeMypost.objects.create(title=title,descrip=descrip,address=address,city=city,district=district,bedroom=bedroom,bathroom=bathroom,name=name,email=email,images=images,user_id = request.user.id,mattien=mattien,chieudai=chieudai,dientich=dientich,solau=solau,addressdetail=addressdetail,chieurong = chieurong,price = price)
        # ,city=city,district=district
        post.save()

        list_images = request.FILES.getlist('list_images')
        for image_file in list_images:
            # Create an Image object and associate it with the post
            image = ListImage.objects.create(listimage=image_file)
            post.listimages.add(image)
            
         # Save the changes to the post
        post.save()
    #display successfull post messages
        messages.success(request, "Your Post has been successfully create")
    #redirect to main page or HomeMypost
        return redirect('post')

    return render(request, 'post.html' )

def show_post(request,event_id):

    event = HomeMypost.objects.get(pk=event_id)
    user_post = User.objects.get(id = event.user_id )  #user profile cua nguoi dang 
    user_profile = UserProfile.objects.get(user_id = event.user_id) #user profile cua nguoi dang 
    listimage = event.listimages.all()
    my_user = request.user   #profile cua nguoi dung dang login
    my_user_profile = UserProfile.objects.get(user_id = my_user.id) 

    comments = Comment.objects.filter(post_id=event_id)

    is_favorite = False
    if my_user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=my_user, post=event).exists()

    if request.method == "POST":
        cmt = request.POST['cmt']
        post_cmt = Comment.objects.create(comment = cmt, user_id = request.user.id, post_id =  event_id, posted_at=datetime.datetime.now() )
        
        post_cmt.save()
    return render(request , "property-single.html" , {'event': event ,'user_post':user_post, 'user_profile' : user_profile, 'comments':comments, 'my_user_profile':my_user_profile,'is_favorite':is_favorite,'listimage':listimage} )
   

   
def profile(request):
    
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        username = request.user.username 
        user = User.objects.get(username = username)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user_profile.fblink = request.POST['facebook']
        user_profile.save()
        user.save()
        if request.FILES.get('profile_pic'):
            user_profile.profile_pic = request.FILES.get('profile_pic')
            user_profile.fblink = request.POST['facebook']
            user_profile.save()
        return redirect('profile')


    return render(request, 'profile.html',  {'user_profile': user_profile})


def review(request):
    if request.method == "POST":
        rating = request.POST.get('rating', None)
        messages = request.POST['mota']
        review = Review.objects.create(review=messages , star = rating , user_id = request.user.id)
    return render(request, 'review.html')


def send_email(request,event_id):
    user = User.objects.get(id = event_id )  #user profile cua nguoi dang 
    if request.method == 'POST':

        subject = request.POST['subject']
        message = request.POST['message']
        from_email = request.user.email
        to_email = [user.email]
        send_mail(subject, message, from_email, to_email , fail_silently=False)


    return render(request, 'send_email.html')

def add_favorite(request):
  
    referer = request.META.get('HTTP_REFERER')  # Get the referring URL
    match = re.search(r'/posts/(\d+)/', referer)  # Match the post_id in the URL

    if match:
        post_id = match.group(1)  # Extract the post_id from the matched result
        print(post_id)
        favorite = Favorite.objects.create(user_id=request.user.id, post_id=post_id)
        favorite.save()

    return redirect(reverse('post_properties', kwargs={'event_id': post_id}))

def remove_favorite(request):
  
    referer = request.META.get('HTTP_REFERER')  # Get the referring URL
    match = re.search(r'/posts/(\d+)/', referer)  # Match the post_id in the URL

    if match:
        post_id = match.group(1)  # Extract the post_id from the matched result

        favorite = Favorite.objects.get(user_id=request.user.id, post_id=post_id)
        favorite.delete()

    return redirect(reverse('post_properties', kwargs={'event_id': post_id}))

def show_favorite(request):
    favorites = Favorite.objects.filter(user_id=request.user.id)
    return render(request, 'favorite.html', {'favorites': favorites})


def becomeahost(request):
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '10.00',
        'item_name': 'Item Name',
        # 'notify_url': 'http://localhost:8000' + reverse('paypal-ipn'),
        'return_url': request.build_absolute_uri(reverse('payment-success')),
        'cancel_return': request.build_absolute_uri(reverse('payment-failed')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    print(form)
    context = {'form': form}
    
    return render(request, 'becomeahost.html', context)

def payment_success(request):
    
    my_user_profile = UserProfile.objects.get(user_id = request.user.id)
    my_user_profile.is_host = 1
    my_user_profile.save()
    return render(request, 'payment_success.html')

def payment_failed(request):

    return render(request, 'payment_failed.html')