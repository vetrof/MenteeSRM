from django.shortcuts import render


def index_page(request):
    return render(request, 'index.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def helpers_page(request):
    return render(request, 'helpers.html')
