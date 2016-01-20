from django.contrib.auth import login, logout,authenticate,get_user_model
from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect,get_object_or_404,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission, User,Group
import logging,csv
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import api_view
from axes.decorators import watch_login
from rest_framework.renderers import TemplateHTMLRenderer
from django.template.context import RequestContext
from django.db.models import Q

from .app_settings import (
    TokenSerializer, UserDetailsSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    PasswordChangeSerializer,LockUserSerializer,UnlockUserSerializer,DeactivateUserSerializer
)

logger = logging.getLogger(__name__)

class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token
    response_serializer = TokenSerializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        print self.user
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        return Response(
            self.response_serializer(self.token).data, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class LogoutView(APIView):

    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class UserDetailsView(RetrieveUpdateAPIView):

    """
    Returns User's details in JSON format.

    Accepts the following GET parameters: token
    Accepts the following POST parameters:
        Required: token
        Optional: email, first_name, last_name and UserProfile fields
    Returns the updated UserProfile and/or User object.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class PasswordResetView(GenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"success": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):

    """
    Password reset e-mail link is confirmed, therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Password has been reset with the new password."})


class PasswordChangeView(GenericAPIView):

    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "New password has been saved."})

class LockUserView(GenericAPIView):

    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/user-view-main.html'
    serializer_class=LockUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = User.objects.get(username=request.GET.get('username'))
        print user
        user.is_active=False;
        user.save()
        #return Response({"success": "User has been locked."})
        queryset = User.objects.all()
        return Response({'userlist': queryset})

class UnlockUserView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/user-view-main.html'
    serializer_class=UnlockUserSerializer
    permission_classes = (AllowAny,)

    def post(self,request):
        user = User.objects.get(username=request.GET.get('username'))
        print user
        user.is_active=True;
        user.save()
        #return Response({"success": "User has been unlocked."})
        queryset = User.objects.all()
        return Response({'userlist': queryset})

class DeactivateUserView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/user-view-main.html'
    serializer_class = DeactivateUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = User.objects.get(username=request.GET.get('username'))
        print user
        user.delete()
        #return Response({"success": "User has been deleted."})
        queryset = User.objects.all()
        return Response({'userlist': queryset})

class UserAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/user-view-main.html'

    def get(self, request,format=None):
        queryset = User.objects.all()
        #usernames = [user.username for user in User.objects.all()]
        return Response({'userlist': queryset})
        #return Response(usernames)

    def post(self, request):
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email=request.POST.get('email')
        user=User.objects.update_or_create(username=username,first_name=firstname,last_name=lastname,email=email)
        queryset = User.objects.all()
        return Response({'userlist': queryset})

    def delete(self,request):
        username=request.GET.get('username')
        user = get_object_or_404(User,username=username)
        user.delete()
        queryset = User.objects.all()
        return Response({'userlist': queryset})

class GroupAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/groupview.html'

    def get(self, request,format=None):
        queryset = Group.objects.all()
        return Response({'grouplist': queryset})

    def post(self, request):
        id = request.POST.get('groupid')
        name = request.POST.get('groupname')
        group=Group.objects.update_or_create(id=id,name=name)
        queryset = Group.objects.all()
        return Response({'grouplist': queryset})

    def delete(self,request):
        name=request.GET.get('groupname')
        group = get_object_or_404(Group,name=name)
        group.delete()
        queryset = Group.objects.all()
        return Response({'grouplist': queryset})

class DeactivateGroupView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/groupview.html'

    def post(self, request):
        group = Group.objects.get(name=request.GET.get('groupname'))
        print group
        group.delete()
        queryset = Group.objects.all()
        return Response({'grouplist': queryset})

class UserSearchAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dashboard/groupedit.html'

    def get(self, request ):
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
                                       context_instance = RequestContext(request))

    def post(self,request):
        x=request.POST.get('checks')
        print x
        name=request.GET.get('groupname')
        id=request.GET.get('id')
        userslist=User.objects.filter(groups__name=name)
        print name
        created = Group.objects.get_or_create(name=name)
        g=Group.objects.get(name=name)
        user = get_object_or_404(User,username=x)
        g.user_set.add(user)
        g.save()
        return Response({'id':id,'name':name,'userslist':userslist})

def handlecsv(request):
    if request.POST and request.FILES:
         csvfile = request.FILES['csv_file']

         print csvfile
         reader = [row for row in csv.reader(csvfile.read().splitlines())]

         header=reader[0]
         if len(reader) > 0:
          header=reader[0]
          reader=reader[1:]
          print header[1],'jkjk'
          if 'username' and 'firstname' in header:
           for row in reader:
            print header.index('username')
            user=User.objects.update_or_create(username=row[header.index('username')],first_name=row[header.index('firstname')],last_name=row[header.index('lastname')],email=row[header.index('email')],password=row[header.index('password')])
         else:
             print 'Canm here'

    return HttpResponseRedirect('/adminuserdetails/')
