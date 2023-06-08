from base64 import urlsafe_b64decode
from email import message
# from email.message import EmailMessage
from gzip import FNAME
# from lib2to3.pgen2.tokenize import generate_tokens
from multiprocessing import context
import re


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
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


#model
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import keras
import seaborn as sns
import matplotlib
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
matplotlib.rcParams["figure.figsize"] = (50,20)
from sklearn.preprocessing import OneHotEncoder
import pickle
import streamlit as st


import os

def get_home(request):
    """
    Handles the request to display the home page.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - Rendered HTML template with the 'post' and 'review' context variables.

    Method:
    - GET: Retrieves and displays all HomeMypost objects and Review objects in descending order of their primary 
    keys.
    - POST: Processes the form data submitted with the request. Filters HomeMypost objects based on the provided 
    city, district, and address parameters.

    Form Parameters (POST request):
    - city: A string representing the city.
    - district: A string representing the district.
    - address: A string representing the ward.

    Returns:
    - Rendered HTML template 'index.html' with the filtered 'post' and 'review' context variables.
    """

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
    """
    Handles the user login request.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - If the user is already authenticated, redirects to the 'home' page.
    - If the request method is POST:
        - Retrieves the username and password from the form data.
        - Attempts to authenticate the user using the provided credentials.
        - If the authentication is successful, logs in the user and returns the result of the 'get_home' 
        function called with the current request.
        - If the authentication fails, displays an error message and renders the 'login.html' template.
    - If the request method is not POST, renders the 'login.html' template.

    Form Parameters (POST request):
    - User: The username provided by the user.
    - Password: The password provided by the user.

    Returns:
    - If the user is already authenticated, redirects to the 'home' page.
    - If the authentication is successful, returns the result of the 'get_home' function called with the 
    current request.
    - If the authentication fails, renders the 'login.html' template with an error message.
    - If the request method is not POST, renders the 'login.html' template.
    """
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
    """
    Handles the user registration request.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - If the user is already authenticated, returns the result of the 'get_home' function 
    called with the current request.
    - If the request method is POST:
        - Retrieves the email, username, first name, last name, and passwords from the form data.
        - Validates the uniqueness of the username and email.
        - Validates the matching of the passwords.
        - Validates that the username is alphanumeric.
        - Creates a new User object with the provided username, email, and password.
        - Sets the first name, last name, and active status for the user.
        - Sends an email confirmation link to the user's email address.
        - Displays a success message and redirects to the 'login' page.
    - If the request method is not POST, renders the 'register.html' template.

    Form Parameters (POST request):
    - Email: The email address provided by the user.
    - User: The username provided by the user.
    - fname: The first name provided by the user.
    - lname: The last name provided by the user.
    - Password1: The first password provided by the user.
    - Password2: The second password provided by the user.

    Returns:
    - If the user is already authenticated, returns the result of the 'get_home' function called with the 
    current request.
    - If the registration is successful, redirects to the 'login' page.
    - If there are validation errors or the request method is not POST, renders the 'register.html' template.
    """
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
    """
    Handles the activation of a user account based on a token and user ID.

    Arguments:
    - request: The HTTP request object.
    - uidb64: The user ID encoded in base 64.
    - token: The activation token.

    Returns:
    - If the user ID and token are valid and match, activates the user account, logs in the user, and redirects 
    to the 'home' page.
    - If the user ID or token is invalid or doesn't match, redirects to the 'activation_fail.html' page.

    Raises:
    - User.DoesNotExist: If the user with the specified ID does not exist.

    Returns:
    - If the activation is successful, redirects to the 'home' page.
    - If the activation fails, redirects to the 'activation_fail.html' page.
    """
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
    """
    Handles the user logout request.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - Logs out the user, displays a success message, and redirects to the 'login' page.
    """
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('login')



def get_all_properties(request):
    """
    Retrieves all posts from the HomeMypost model and displays them in a paginated manner.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - Renders the 'properties.html' template with the paginated 'posts' context variable.

    Pagination:
    - The number of posts per page can be adjusted by modifying the 'Paginator' line in the code (default: 1).
    - The current page number is retrieved from the request's GET parameters using the key 'page'.
    - The retrieved posts are paginated using the 'Paginator' object and the requested page number.
    - The paginated posts are passed to the 'properties.html' template as the 'posts' context variable.
    """
    all_posts = HomeMypost.objects.order_by('-pk')

    paginator = Paginator(all_posts, 3)  # Adjust the number of posts per page as needed

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'properties.html', {'posts': posts})



def post(request):
    """
    Handles the creation of a post.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - If the user is not authenticated, redirects to the 'login' page.
    - If the request method is POST:
        - Retrieves the post data from the form.
        - Creates a new HomeMypost object with the provided data.
        - Associates the post with the authenticated user.
        - Saves the post to the database.
        - Saves the list of images associated with the post.
        - Displays a success message and redirects to the 'post' page.
    - If the request method is not POST, renders the 'post.html' template.

    Form Parameters (POST request):
    - tieude: The title of the post.
    - mota: The description of the post.
    - address: The address (ward) of the post.
    - city: The city of the post.
    - district: The district of the post.
    - addressdetail: The detailed address of the post.
    - mattien: The material type of the post.
    - price: The price of the post.
    - cd: The length of the post.
    - cr: The width of the post.
    - dt: The area of the post.
    - name: The name of the user.
    - email: The email address of the user.
    - bedroom: The number of bedrooms in the post.
    - bathroom: The number of bathrooms in the post.
    - solau: The number of floors in the post.
    - images: The main image of the post.
    - list_images: The list of additional images for the post.

    Returns:
    - If the creation is successful, redirects to the 'post' page.
    - If there are validation errors or the request method is not POST, renders the 'post.html' template.
    """
    if request.user.is_authenticated == False:
        return redirect('login') 

  



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
        crd = request.POST['crd']

        images = request.FILES.get('images')

        user_input_quan = district
        quan_1 = " " + user_input_quan

        user_input_phuong = address
        phuong = " " + user_input_phuong

    
        user_input_loaibds = mattien
        loaibds = " " + user_input_loaibds

        user_input_dt = dientich
        dt =  float(user_input_dt)

        user_input_cd = chieudai
        cd =  float(user_input_cd)

        user_input_cn = chieurong
        cn = float(user_input_cn)

        user_input_duongtruocnha = crd
        duongtruocnha = float(user_input_duongtruocnha)

        user_input_phongngu = bedroom
        phongngu = float(user_input_phongngu)

        user_input_solau = bathroom
        solau = float(user_input_solau)

        array_data = [dt,duongtruocnha,phongngu,cd,cn,solau,loaibds,phuong]

        result = build_model_estimate(quan_1,array_data)

        #save post to db
        post = HomeMypost.objects.create(title=title,descrip=descrip,address=address,city=city,district=district,bedroom=bedroom,bathroom=bathroom,name=name,email=email,images=images,user_id = request.user.id,mattien=mattien,chieudai=chieudai,dientich=dientich,solau=solau,addressdetail=addressdetail,chieurong = chieurong,price = price,duongtruocnha = duongtruocnha,guess_price = result[1]*1_000_000_000,dochinhxac = result[2]*100)
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
        return render(request, 'post.html' )

    return render(request, 'post.html' )





def build_model_estimate(quan,arr):
    csv_filename = os.path.join(os.path.dirname(__file__), 'static/data/data_predict.csv')
    dataset = pd.read_csv(csv_filename,low_memory=False)
    dataset = dataset.dropna()
    encoder = OneHotEncoder(handle_unknown='ignore')
    df1 = dataset[dataset["quan"] == quan]   
    df1 = df1.reset_index(drop=True)
    encoder_df_dummies = pd.get_dummies(df1, columns = ['loaibds','phuong'])
    
    # final_df = df1.join(encoder_df)
    # final_df
    x1 = encoder_df_dummies.drop(columns=['quan','gia'])
  
    y1 = encoder_df_dummies[['gia']]
    X_train, X_test, y_train, y_test = train_test_split(x1, y1, test_size=0.2, random_state=110)
    lm = LinearRegression()
    reg = lm.fit(X_train,y_train)
    predictions = lm.predict(X_test)
    # print('MAE:', metrics.mean_absolute_error(y_test, predictions)) 
    # print('MSE:', metrics.mean_squared_error(y_test, predictions)) 
    # print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))
    r2_score = lm.score(X_test,y_test)
    print(r2_score*100,'%')
    arr1 = []
    i = 0
    arr1.clear()
    count_column = 0
    for i in range(x1.shape[1]):
        if(i < 6):
            arr1.append(arr[i])
        else:
            if (i < 8):
                str1 = x1.columns[i]
                str2 = arr[6]
                if(str2 in str1):
                    arr1.append(1)
                else:
                    arr1.append(0)
            else:
                str1 = x1.columns[i]
                str2 = arr[7]
                if(str2 in str1):
                    arr1.append(1)
                else:
                    arr1.append(0)
    test_data = np.array(arr1)
    return lm,lm.predict(test_data.reshape(1,x1.shape[1]))[0][0],r2_score

def show_post(request,event_id):
    """
    Displays a single post along with its details, comments, and related user profiles.

    Arguments:
    - request: The HTTP request object.
    - event_id: The ID of the post to display.

    Returns:
    - If the request method is POST:
        - Retrieves the comment data from the form.
        - Creates a new Comment object associated with the post and the authenticated user.
        - Saves the comment to the database.
    - Retrieves the post, user profile of the post creator, user profile of the logged-in user (if available),
      comments, and list of images associated with the post.
    - Checks if the post is marked as a favorite by the logged-in user.
    - Renders the 'property-single.html' template with the retrieved data.

    Note:
    - The user profile of the logged-in user may be set to None if the UserProfile object doesn't exist.

    Form Parameters (POST request):
    - cmt: The comment text.

    Returns:
    - Renders the 'property-single.html' template with the post details, user profiles, comments,
      and related data.
    """
    my_user_profile = None  # Initialize with a default value
    event = HomeMypost.objects.get(pk=event_id)
    user_post = User.objects.get(id = event.user_id )  #user profile cua nguoi dang 
    user_profile = UserProfile.objects.get(user_id = event.user_id) #user profile cua nguoi dang bai
    listimage = event.listimages.all()
    my_user = request.user   #profile cua nguoi dung dang login
    comments = Comment.objects.filter(post_id=event_id)
    try :
        my_user_profile = UserProfile.objects.get(user_id = my_user.id) 

   
    except UserProfile.DoesNotExist:
        # Handle the case when UserProfile doesn't exist
        user_profile = None  # Set user_profile to None or any default value you prefer

    is_favorite = False
    if my_user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=my_user, post=event).exists()

    if request.method == "POST":
        cmt = request.POST['cmt']
        post_cmt = Comment.objects.create(comment = cmt, user_id = request.user.id, post_id =  event_id, posted_at=datetime.datetime.now() )
        
        post_cmt.save()
    return render(request , "property-single.html" , {'event': event ,'user_post':user_post, 'user_profile' : user_profile, 'comments':comments, 'my_user_profile':my_user_profile,'is_favorite':is_favorite,'listimage':listimage} )
   

@login_required(login_url='login')  # Specify the URL of the login page
def profile(request):
    """
    Handles the user profile page.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - If the request method is POST:
        - Updates the user's first name, last name, email, profile picture, and Facebook link based on the
          submitted form data.
        - Redirects to the 'profile' page.
    - Retrieves the user's profile and checks if it exists. If not, creates a new profile.
    - Renders the 'profile.html' template with the user's profile data.

    Form Parameters (POST request):
    - first_name: The user's first name.
    - last_name: The user's last name.
    - email: The user's email address.
    - profile_pic: The user's profile picture.
    - facebook: The user's Facebook link.

    Returns:
    - If the request method is POST, redirects to the 'profile' page.
    - If the request method is not POST, renders the 'profile.html' template with the user's profile data.
    """
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


@login_required(login_url='login')  # Specify the URL of the login page
def my_post(request):

    all_posts_s = HomeMypost.objects.order_by('id')
    paginator = Paginator(all_posts_s, 2)  # Adjust the number of posts per page as needed
    page_number = request.GET.get('page')
    mypost = paginator.get_page(page_number)

    return render(request, 'mypost.html',  {'mypost': mypost})


@login_required(login_url='login')  # Specify the URL of the login page
def delete_item(request, item_id):
    item = get_object_or_404(HomeMypost, id=item_id)
    item.delete()
    return my_post(request)


@login_required(login_url='login')  # Specify the URL of the login page
def review(request):
    """
    Handles the review page.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - If the request method is POST:
        - Retrieves the rating and review message from the submitted form data.
        - Creates a new Review object associated with the authenticated user.
    - Renders the 'review.html' template.

    Form Parameters (POST request):
    - rating: The rating value.
    - mota: The review message.

    Returns:
    - If the request method is POST, no explicit return value.
    - If the request method is not POST, renders the 'review.html' template.
    """
    if request.method == "POST":
        rating = request.POST.get('rating', None)
        messages = request.POST['mota']
        review = Review.objects.create(review=messages , star = rating , user_id = request.user.id)
    return render(request, 'review.html')

@login_required(login_url='login')  # Specify the URL of the login page
def send_email(request,event_id):
    """
    Handles sending an email to a user.

    Arguments:
    - request: The HTTP request object.
    - event_id: The ID of the user to whom the email will be sent.

    Returns:
    - If the request method is POST:
        - Retrieves the subject and message from the submitted form data.
        - Sends an email from the authenticated user's email address to the user with the specified event ID.
    - Renders the 'send_email.html' template.

    Form Parameters (POST request):
    - subject: The subject of the email.
    - message: The content of the email.

    Returns:
    - If the request method is POST, no explicit return value.
    - If the request method is not POST, renders the 'send_email.html' template.
    """
    user = User.objects.get(id = event_id )  #user profile cua nguoi dang 
    if request.method == 'POST':

        subject = request.POST['subject']
        message = request.POST['message']
        from_email = request.user.email
        to_email = [user.email]
        send_mail(subject, message, from_email, to_email , fail_silently=False)


    return render(request, 'send_email.html')

@login_required(login_url='login')  # Specify the URL of the login page
def add_favorite(request):
    """
    Adds a post to the user's favorites.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - If the referring URL contains a valid post ID:
        - Extracts the post ID from the referring URL.
        - Creates a new Favorite object associated with the authenticated user and the extracted post ID.
    - Redirects the user to the 'post_properties' view with the extracted post ID as a parameter.

    Returns:
    - If the referring URL contains a valid post ID, no explicit return value.
    - If the referring URL doesn't contain a valid post ID, the behavior is unspecified.
    """
    referer = request.META.get('HTTP_REFERER')  # Get the referring URL
    match = re.search(r'/posts/(\d+)/', referer)  # Match the post_id in the URL

    if match:
        post_id = match.group(1)  # Extract the post_id from the matched result
        print(post_id)
        favorite = Favorite.objects.create(user_id=request.user.id, post_id=post_id)
        favorite.save()

    return redirect(reverse('post_properties', kwargs={'event_id': post_id}))

@login_required(login_url='login')  # Specify the URL of the login page
def remove_favorite(request):
    """
    Removes a post from the user's favorites.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - If the referring URL contains a valid post ID:
        - Extracts the post ID from the referring URL.
        - Retrieves the Favorite object associated with the authenticated user and the extracted post ID.
        - Deletes the retrieved Favorite object.
    - Redirects the user to the 'post_properties' view with the extracted post ID as a parameter.

    Returns:
    - If the referring URL contains a valid post ID, no explicit return value.
    - If the referring URL doesn't contain a valid post ID or the Favorite object doesn't exist, 
    the behavior is unspecified.
    """
    referer = request.META.get('HTTP_REFERER')  # Get the referring URL
    match = re.search(r'/posts/(\d+)/', referer)  # Match the post_id in the URL

    if match:
        post_id = match.group(1)  # Extract the post_id from the matched result

        favorite = Favorite.objects.get(user_id=request.user.id, post_id=post_id)
        favorite.delete()

    return redirect(reverse('post_properties', kwargs={'event_id': post_id}))

def show_favorite(request):
    """
    Retrieves and displays the favorite posts of the authenticated user.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - Renders the 'favorite.html' template with the retrieved favorite posts.

    Notes:
    - The function retrieves the favorite posts associated with the authenticated user by
      filtering the Favorite objects based on the user's ID.
    - The retrieved favorite posts are passed to the 'favorite.html' template for rendering.
    """
    favorites = Favorite.objects.filter(user_id=request.user.id)
    return render(request, 'favorite.html', {'favorites': favorites})



@login_required(login_url='login')  # Specify the URL of the login page
def becomeahost(request):
    """
    Handles the request for becoming a host.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - Renders the 'becomeahost.html' template with the PayPalPaymentsForm.

    Notes:
    - The function generates a PayPal payment form using the PayPalPaymentsForm class.
    - The PayPal form is pre-filled with the necessary details such as the receiver email, 
    amount, item name, return URL, and cancel return URL.
    - The rendered form is passed to the 'becomeahost.html' template for display.
    """
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
    
    """
    Handles the payment success callback.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - Renders the 'payment_success.html' template.

    Notes:
    - Retrieves the user profile for the logged-in user using UserProfile.objects.get().
    - Sets the 'is_host' attribute of the user profile to 1 (indicating the user is now a host).
    - Saves the changes to the user profile.
    - Renders the 'payment_success.html' template.
    """
    my_user_profile = UserProfile.objects.get(user_id = request.user.id)
    my_user_profile.is_host = 1
    my_user_profile.save()
    return render(request, 'payment_success.html')

def payment_failed(request):
    """
    Handles the payment failure callback.

    Arguments:
    - request: The HTTP request object.

    Returns:
    - Renders the 'payment_failed.html' template.

    Notes:
    - Renders the 'payment_failed.html' template to display a message or instructions
    for the payment failure.
    """
    return render(request, 'payment_failed.html')