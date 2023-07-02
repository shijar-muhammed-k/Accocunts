from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import models
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from datetime import datetime



# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pswd']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('admin_home')
        else:
            return render(request, 'login.html', {'msg' : True})
    return render(request, 'login.html')


@login_required()
def admin_home(request):
    print(request.path)
    return render(request, 'admin/home.html')


@login_required()
def staffs(request):
    db = models.Staffs.objects.all()
    return render(request, 'admin/staffs.html', {'staffs': db})


@login_required()
def add_staff(request):
    try:
        if request.method == 'POST':
            staff_db = models.Staffs()
            staff_db.firstName = request.POST['firstName']
            staff_db.lastName = request.POST['lastName']
            staff_db.email = request.POST['email']
            staff_db.phoneNumber = request.POST['phone']
            staff_db.gender = request.POST['gender']
            staff_db.address = request.POST['address']
            staff_db.profile_picture = request.FILES['profile_picture']
            staff_db.attachment = request.FILES['attachment']
            staff_db.save()
            return redirect('staffs')
    except:
        return HttpResponse("<script>alert('Sorry Something Went Wrong')</script>")    
    return render(request, 'admin/add_staff.html')



def expences(request):
    data = models.Expences.objects.all()
    return render(request, 'admin/expences.html', {'data': data})


def add_expences(request):
    db = models.Expences()
    db.Purchase = request.POST['purchase']
    db.Remark = request.POST['remark']
    db.Amount = request.POST['amount']
    db.save()
    return redirect('expences')


def returns(request):
    return render(request, 'admin/returns.html')


def editStaff(request, id):
    db = models.Staffs.objects.get(id = id)
    if request.method == 'POST':
        db.firstName = request.POST['firstName']
        db.lastName = request.POST['lastName']
        db.email = request.POST['email']
        db.phoneNumber = request.POST['phone']
        db.address = request.POST['address']
        db.gender = request.POST['gender']
        try:
            if request.FILES['profile_picture']:
                db.profile_picture = request.FILES['profile_picture']
        except:
            pass
        try:
            if request.FILES['attachment']:
                db.attachment = request.FILES['attachment']
        except:
            pass
        db.save()
        return redirect('staffs')
    
    return render(request, 'admin/add_staff.html', {'data' : db})