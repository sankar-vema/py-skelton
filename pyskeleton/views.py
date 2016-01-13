__author__ = 'agupta330'
from django.contrib.auth.models import Permission, User,Group
from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,render_to_response
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.db.models import Q

@login_required
def index(request):
    userlist=User.objects.all()
    print userlist
    return render(request,'dashboard/index.html',{'userlist':userlist})

@login_required
def ajax_user_search( request ):
    grouplist=Group.objects.all()
    userlist=User.objects.all()
    print grouplist,userlist
    if request.is_ajax():
        q = request.GET.get( 'q' )
        if q is not None:
            results = User.objects.filter(
                Q( username__contains = q ) ).order_by( 'username' )

            template = 'dashboard/results.html'
            data = {
                'results': results,'grouplist':grouplist
            }
            return render_to_response( template, data,
                                       context_instance = RequestContext( request ) )

# Logout Functionality
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def adminuserdetails(request):
    userlist=User.objects.all()
    print userlist
    return render(request,'dashboard/user-view-main.html',{'userlist':userlist})

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

@login_required
def admingroups(request):
    grouplist=Group.objects.all()
    userlist=User.objects.all()
    print grouplist,userlist
    return render(request,'dashboard/groupview.html',{'grouplist':grouplist,'userlist':userlist})

@login_required
def savegroup(request):
    if request.method == 'POST':
        id = request.POST.get('groupid')
        name = request.POST.get('groupname')
        group=Group.objects.update_or_create(id=id,name=name)

    return HttpResponseRedirect('/admingroups/')

@login_required
def deactivategroup(request):
    name=request.GET.get('groupname')
    group = get_object_or_404(Group,name=name)
    group.delete()
    return HttpResponseRedirect('/admingroups/')

@login_required
def addusertogroup(request):
    x=request.POST.get('checks')
    print x
    #z=[str(y) for y in x]
    name=request.GET.get('groupname')
    id=request.GET.get('id')
    userslist=User.objects.filter(groups__name=name)
    print name
   # print len(z)
    #user=User.objects.get(username=x[0].encode('utf8'))
    #for i in range(len(z)):
    created = Group.objects.get_or_create(name=name)
    g=Group.objects.get(name=name)
    user = get_object_or_404(User,username=x)
    g.user_set.add(user)
    g.save()
   # return HttpResponseRedirect('/admingroups/')
    return render(request,'dashboard/groupedit.html',{'id':id,'name':name,'userslist':userslist})

@login_required
def editgroup(request):
    name=request.GET.get('groupname')
    id=request.GET.get('id')
    group = get_object_or_404(Group,name=name)
    userslist=User.objects.filter(groups__name=name)
    print userslist
    print id,group
    return render(request,'dashboard/groupedit.html',{'id':id,'name':name,'userslist':userslist})

@login_required
def deleteuserfromgroup(request):
    username=request.GET.get('username')
    name=request.GET.get('groupname')
    id=request.GET.get('id')
    user=get_object_or_404(User,username=username)
    userslist=User.objects.filter(groups__name=name)
    print username,name,id
    g=get_object_or_404(Group,name=name)
    print g
    g.user_set.remove(user)
    g.save()
    return render(request,'dashboard/groupedit.html',{'id':id,'name':name,'userslist':userslist})
