from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def index(request):
	return render(request, 'students/index.html')

def login(request):
    return render(request, 'students/login.html')

def logout(request):
    logout(request)
    return render(request, 'students/index.html')
