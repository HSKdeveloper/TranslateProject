from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

#Sign up view
def sign_up(request:HttpRequest):

    if request.method == "POST":
        try:
           # with transaction.atomic():
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()
            messages.success(request,"Registered user successfuly", "alert-success")

            return redirect("accounts:sign_in")
        
        except Exception as e:
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
            return redirect("accounts:test_view")
        else:
            messages.error(request," Please try again. You credentials are wrong", "alert-danger")

    return render(request, "accounts/signin.html")


#Logout view
def logout (request:HttpRequest):

    logout(request)
    messages.success(request, "logged out successfuly", "alert-success")
    return redirect("accounts:test_view")

    

#test page
def test_view(request:HttpRequest):

    if request.user.is_authenticated:
        print(request.user.email)
    else:
        print("user is not logged in")

    return render(request, "accounts/test.html")

#Profile view
def profile_view(request:HttpRequest):

    return render(request, "accounts/profile.html")

#Profile update view
def update_profile_view(request:HttpRequest):

    return render(request, "accounts/update_profile.html")