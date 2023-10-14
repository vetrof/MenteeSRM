from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

from login_app.forms import LoginForm


def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')

            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})