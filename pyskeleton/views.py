__author__ = 'agupta330'
from django.contrib.auth.models import Permission, User
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    userlist=User.objects.all()
    print userlist
    return render(request,'index.html',{'userlist':userlist})

# Logout Functionality
@login_required
def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/')

@login_required
def adminuserdetails(request):
    userlist=User.objects.all()
    print userlist
    return render(request,'user-view-main.html',{'userlist':userlist})

@login_required
def saveuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email=request.POST.get('email')
        user=User.objects.update_or_create(username=username,first_name=firstname,last_name=lastname,email=email)

    return HttpResponseRedirect('/adminuserdetails/')

@login_required
def lockuser(request):
    username=request.GET.get('username')
    user = User.objects.get(username=username)
    print user
    user.is_active=False;
    user.save()
    return HttpResponseRedirect('/adminuserdetails/')

@login_required
def unlockuser(request):
    username=request.GET.get('username')
    user = User.objects.get(username=username)
    print user
    user.is_active=True;
    user.save()
    return HttpResponseRedirect('/adminuserdetails/')

@login_required
def deactivateuser(request):
    username=request.GET.get('username')
    user = get_object_or_404(User,username=username)
    user.delete()
    return HttpResponseRedirect('/adminuserdetails/')