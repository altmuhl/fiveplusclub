from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.views import index
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse

from products.models import Basket
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': UserLoginForm()}
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/regisrtation.html', context)
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance= request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    baskets = Basket.objects.filter(user=request.user)
    context = {
        'title': 'ЦТН - Профиль',
        'form': form,
        'baskets': baskets,

    }
    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))