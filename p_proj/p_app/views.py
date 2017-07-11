from django.shortcuts import render
from p_app.forms import UserSignupForm, UserProfileInfoForm
from p_app import models
from django.contrib.auth.models import User

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required



def index(req):
    return render(req,"p_app/index.html")


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))



def users(req):
    usrLst = models.User.objects.order_by('first_name')
    return render(req,"p_app/user.html",{'users':usrLst})

def signup(req):
    usrfrm = UserSignupForm()
    prfrm =  UserProfileInfoForm()
    if req.method == 'POST':
        usrfrm = UserSignupForm(req.POST)
        prfrm =  UserProfileInfoForm(req.POST)

        if usrfrm.is_valid and prfrm.is_valid:
            user = usrfrm.save()
            prf = prfrm.save(commit=False)
            prf.user = user
            if 'profile_pic' in req.FILES:
                prf.profile_pic = req.FILES['profile_pic']
            prf.save()

    return render(req,"p_app/signup.html",{"form":usrfrm,'form2':prfrm})

def usr_login(request):
        if request.method == 'POST':
            # First get the username and password supplied
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)

            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to some page.
                    # In this case their homepage.
                    return HttpResponseRedirect(reverse('index'))
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return HttpResponse("Invalid login details supplied.")

        else:
            #Nothing has been provided for username or password.
            return render(request, 'p_app/usr_login.html',{})
