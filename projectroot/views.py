from django.shortcuts import render


def home(request):
    
    return render(request, 'home/index_page.html')