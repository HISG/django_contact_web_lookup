from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.http import urlquote, base36_to_int
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from tiqLibraries.tiqErrors import TiqPasswordExpiredError
from tiq_login import getSessionRpcClient
from django.core.urlresolvers import reverse
from settings import *
from forms import PasswordChangeForm

def login(request, template_name=TIQ_LOGIN_TEMPLATE_LOGIN, redirect_field_name=REDIRECT_FIELD_NAME):
    "Displays the login form and handles the login action."

    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        try:
           if form.is_valid():
               # Light security check -- make sure redirect_to isn't garbage.
               if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                   redirect_to = LOGIN_REDIRECT_URL
               from django.contrib.auth import login
               login(request, form.get_user())
               
               if request.session.test_cookie_worked():
                   request.session.delete_test_cookie()
               return HttpResponseRedirect(redirect_to)

        except TiqPasswordExpiredError, e:
           return HttpResponseRedirect(reverse(PATH_TO_THIS_MODULE + '.views.password_change'))
     
    else:
       form = AuthenticationForm(request)

    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

login = never_cache(login)


def logout(request, next_page=None, template_name=TIQ_LOGIN_TEMPLATE_LOGGED_OUT):
    "Logs out the user and displays 'You are logged out' message."

    profile = request.user.get_profile()

    sessionRpcClient = getSessionRpcClient(profile.session_id)
    sessionRpcClient.execute('logout')
  
    profile.session_id = ''
    profile.save()

    from django.contrib.auth import logout
    logout(request)
    if next_page is None:
        return render_to_response(template_name, {'title': _('Logged out'), 'login_link': LOGIN_URL}, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

def logout_then_login(request, login_url=None):
    "Logs out the user if he is logged in. Then redirects to the log-in page."
    if not login_url:
        login_url = LOGIN_URL
    return logout(request, login_url)

def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    "Redirects the user to the login page, passing the given 'next' page"
    if not login_url:
        login_url = LOGIN_URL
    return HttpResponseRedirect('%s?%s=%s' % (login_url, urlquote(redirect_field_name), urlquote(next)))


def password_change(request, template_name=TIQ_LOGIN_TEMPLATE_PASSWORD_CHANGE,
                    post_change_redirect=LOGIN_REDIRECT_URL):

    login_error = None

    if request.method == "POST":

       form = PasswordChangeForm(request.POST)
       if form.is_valid():
          
          # TODO TIQ PASSWORD CHANGE CODE HERE
          username = form.cleaned_data['username']
          old_password = form.cleaned_data['old_password']
          new_password = form.cleaned_data['new_password_1']
          
          sessionRpcClient = getSessionRpcClient()
          try:
             sessionRpcClient.changePassword(username, old_password, new_password)
          except Exception, e:
             form = PasswordChangeForm()
             login_error = "Your username and old password are incorrect."
             print str(form.errors) + "<- ***"
          else:
             # not catching errors here, assuming that if the password change succeeded that this will too
             from django.contrib.auth import authenticate, login
             user = authenticate(username=username, password=new_password)
             login(request, user)
             return HttpResponseRedirect(post_change_redirect)
      
    else:
        form = PasswordChangeForm()
        
    return render_to_response(template_name, {
        'form': form, 'login_error': login_error
    }, context_instance=RequestContext(request))


def password_change_done(request, template_name=TIQ_LOGIN_TEMPLATE_PASSWORD_CHANGE_DONE):
    return render_to_response(template_name, context_instance=RequestContext(request))
