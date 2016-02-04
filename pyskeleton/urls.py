from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required
from pyskeleton import views
#from axes.decorators import watch_login
from allauth.account.views import login

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="dashboard/home.html"), name='home'),

    #url(r'^index/$',TemplateView.as_view(template_name="index.html"), name='index'),

    url(r'^index/$',views.index,name='index'),

    url(r'^signup/$', TemplateView.as_view(template_name="auth/signup.html"), name='signup'),

    url(r'^email-verification/$',TemplateView.as_view(template_name="auth/email_verification.html"),name='email-verification'),

    url(r'^login/$', TemplateView.as_view(template_name="auth/login.html"),name='login'),

    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^lockuser/$',views.lockuser,name='lockuser'),

    url(r'^unlockuser/$',views.unlockuser,name='unlockuser'),

    url(r'^deactivateuser/$',views.deactivateuser,name='deactivateuser'),

    url(r'^deactivategroup/$',views.deactivategroup,name='deactivategroup'),

    url(r'^addusertogroup/$',views.addusertogroup,name='addusertogroup'),

    url(r'^password-reset/$',TemplateView.as_view(template_name="auth/password_reset.html"),name='password-reset'),

    url(r'^password-reset/confirm/$',TemplateView.as_view(template_name="auth/password_reset_confirm.html"),name='password-reset-confirm'),

    url(r'^password-change/$',TemplateView.as_view(template_name="auth/password_change.html"),name='password-change'),

    url(r'^user-details/$',TemplateView.as_view(template_name="dashboard/user_details.html"),name='user-details'),

    url(r'^adminuserdetails/$',views.adminuserdetails,name='adminuserdetails'),

    url(r'^admingroups/$',views.admingroups,name='admingroups'),

    url(r'^saveuser/$',views.saveuser,name='saveuser'),

    url(r'^savegroup/$',views.savegroup,name='savegroup'),

    url(r'^editgroup/$',views.editgroup,name='editgroup'),

    url(r'^deleteuserfromgroup/$',views.deleteuserfromgroup,name='deleteuserfromgroup'),

    #url( r'^index1/$', views.index1, name = 'demo_index' ),
	url( r'^users/$', views.ajax_user_search, name = 'demo_user_search' ),

    # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="auth/password_reset_confirm.html"),name='password_reset_confirm'),

    url(r'^rest-auth/', include('rest_auth.urls')),

    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

    #url(r'^accounts/login/$', watch_login(login)),

    #url(r'^accounts/login/$', login),
    url(r'^account/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/profile/$', RedirectView.as_view(url='/', permanent=True), name='profile-redirect'),
]
