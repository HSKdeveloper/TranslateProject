from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib import messages
from django.db import transaction


# Create your views here.

#Sign up view
def sign_up(request:HttpRequest):

    if request.method == "POST":
        try:
           with transaction.atomic():
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()

            #create user profile
            profile=Profile(user=new_user, bio=request.POST["bio"],user_type=request.POST["user_type"], avatar=request.FILES.get("avatar", Profile.avatar.field.get_default()))
            profile.save()

            messages.success(request, "Registered user successfuly", "alert-success")
            return redirect("accounts:sign_in")
        except Exception as e:
            messages.error(request, "Couldn't register user, please try again", "alert-danger")
            print(e)
            
    
    return render(request, "accounts/signup.html")

#Sign in view
def sign_in(request:HttpRequest):

    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfuly", "alert-success")
            return redirect("main:home_view")
        else:
            messages.error(request," Please try again. You credentials are wrong", "alert-danger")

    return render(request, "accounts/signin.html")


#Logout view
def log_out (request:HttpRequest):

    logout(request)
    messages.success(request, "logged out successfuly", "alert-warning")

    return redirect('main:home_view')


#Profile view
def profile_view(request:HttpRequest):

    try:
        user = User.objects.get(username=request.user.username)

        
    except :
        return render(request, "accounts/404.html")

    return render(request, "accounts/profile.html", {"user": user})

#Profile update view
def update_profile_view(request:HttpRequest):

    if not request.user.is_authenticated:
        messages.warning(request, "You need to sign in first to update your profile", "alert-warning")
        return redirect("accounts:sign_in")
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                user:User = request.user
                user.first_name=request.POST['first_name']
                user.last_name=request.POST['last_name']
                user.email=request.POST['email']
                user.save()

                profile:Profile = user.profile
                profile.bio=request.POST['bio']
                profile.avatar=request.FILES.get('avatar', profile.avatar)
                profile.save()

            messages.success(request, "Profile updated successfuly", "alert-success")

        except Exception as e:
            messages.error(request, "Couldn't update profile, please try again", "alert-danger")
            print(e)
        return redirect("accounts:profile_view")
    
    return render(request, "accounts/update_profile.html")