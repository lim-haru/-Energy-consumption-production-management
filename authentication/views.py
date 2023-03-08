from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from .utils import checkIp
from .models import SessionHistory
from django.core.cache import cache

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            checkIp(request)
            messages.success(request, f"Login effettuato con successo. Benvenuto {user}!")
            cache.delete('table-session')
            return redirect('home')
        else:
            messages.error(request, "Username o password non corretti")
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Il tuo account è stato scollegato")
    return redirect('home')

def settings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            passOld = request.POST['passOld']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if pass1 != pass2:
                messages.error(request, 'Le nuove password non corrispondono')

            elif len(pass1)<8:
                messages.error(request, 'La nuova password deve contenere almeno 8 caratteri')

            elif not check_password(passOld, request.user.password):
                messages.error(request, 'La password attuale è sbagliata')

            elif passOld == pass1:
                messages.error(request, 'La nuova password è uguale a quella vecchia')

            else:
                myuser = User.objects.get(username=request.user)
                myuser.set_password(pass1)
                myuser.save()

                messages.success(request, 'La nuova password è stata aggiornata')
                return redirect('signout')

        if cache.get('table-session'):
            sessions = cache.get('table-session')
        else:
            sessions = SessionHistory.objects.all().order_by('-date')
            #cache.set table-session su html

        token, created = Token.objects.get_or_create(user=request.user)
        return render(request, 'settings.html', {'token': token.key, 'sessions': sessions})
    else:
        return render(request, 'home.html')


