from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import models


# Create your views here.
def login(request):
    if request.method == 'POST':
        return redirect('admin_home')
    return render(request, 'login.html')

def admin_home(request):
    print(request.path)
    return render(request, 'admin/home.html')

def staffs(request):
    return render(request, 'admin/staffs.html')

def add_staff(request):
    return render(request, 'admin/add_staff.html')