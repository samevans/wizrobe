from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from .forms import RegistrationForm

def home(request):
    args = {'request':request}
    if request.user.is_authenticated is not AnonymousUser:
        args['user'] = request.user
    
    return render(request, 'home.html', args)


@login_required(login_url='/login')
def dashboard(request):
    args = {'request':request}
    if request.user.is_authenticated is not AnonymousUser:
        args['user'] = request.user
    
    return render(request, 'dashboard.html', args)


def contactus(request):
    args = {'request':request}
    if request.user.is_authenticated is not AnonymousUser:
        args['user'] = request.user
    
    return render(request, 'contactus.html', args)


@login_required(login_url='/login')
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            save_signup = form.save(commit=False)
            save_signup.save()
            
            if settings.EMAILS_ON:
                subject = 'Create account validation'
                message = 'Welcome to Wizrobe.'
                from_email = settings.EMAIL_HOST_USER
                to_list = [save_signup.email, settings.EMAIL_HOST_USER]
                send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            messages.success(request, 'We have received your request. Please validate through your email.')
            return HttpResponseRedirect('/login')
        else:
            print form.is_valid(), form.errors, type(form.errors)
    else:
        form = RegistrationForm()
        
    args = {'form': form, 'request': request}

    return render(request, 'signup.html', args)


def requestpassword(request):
    args = {'request':request}
    if request.user.is_authenticated is not AnonymousUser:
        args['user'] = request.user
    
    return render(request, 'requestpassword.html', args)


@login_required(login_url='/login')
def view_profile(request):
    args = { 'user': request.user, 'request': request }
    return render(request, 'profile.html', args)


@login_required(login_url='/login')
def edit_profile(request):
    args = { 'user': request.user, 'request': request }
    return render_to_response("profile_edit.html", locals(), context_instance=RequestContext(request))


@login_required(login_url='/login')
def successfully_loggedin(request):
    return HttpResponseRedirect('/profile')
    # return HttpResponseRedirect('/dashboard')