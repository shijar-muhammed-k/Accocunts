import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import models
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q, Sum, Avg
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pswd')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            if(username == 'shijar'):
                request.session['user_role'] = 'admin'
            else:
                user = models.Staffs.objects.get(email = username)
                if(user.status == False):
                    return HttpResponse('<script>alertI"User is not authorized"); window.location("login")</script>')
                request.session['user_access'] = user.access
                request.session['user_id'] = user.id
            return redirect('admin_home')
        else:
            return render(request, 'login.html', {'msg' : True})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required()
def admin_home(request):
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
            staff_db.firstName = request.POST.get('firstName')
            staff_db.lastName = request.POST.get('lastName')
            staff_db.email = request.POST.get('email')
            staff_db.phoneNumber = request.POST.get('phone')
            staff_db.gender = request.POST.get('gender')
            staff_db.address = request.POST.get('address')
            staff_db.profile_picture = request.FILES['profile_picture']
            staff_db.attachment = request.FILES['attachment']
            staff_db.shift = request.POST.get('shift')
            staff_db.save()
            user = User.objects.create_user(username=staff_db.email, password=staff_db.phoneNumber)
            user.save()
            return redirect('staffs')
    except:
        return HttpResponse("<script>alert('Sorry Something Went Wrong'); window.location('login')</script>")    
    return render(request, 'admin/add_staff.html')


@login_required()
def expences(request):
    if request.method == 'POST':
        db = models.Expences()
        db.Purchase = request.POST.get('purchase')
        db.Remark = request.POST.get('remark')
        db.Amount = request.POST.get('amount')
        db.save()
        return redirect('expences')
    

    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    search = request.GET.get('search')
    current_month = datetime.now().month
    data = models.Expences.objects.filter(Date__month=current_month)

    current_month = datetime.now().strftime('%B')
    if fromDate and toDate:
        data = data.filter(Q(Date__gte=fromDate) & Q(Date__lte=toDate))
        current_month = f'{fromDate} - {toDate}' 
    elif fromDate:
        data = data.filter(Date__gte=fromDate)
        current_month = f'{fromDate} - '
    elif toDate:
        data = data.filter(Date__lte=toDate)
        current_month = f' - {toDate}'
    if search:
        data = data.filter(Q(Purchase__icontains=search))
    
    sum_amount = data.aggregate(sum_amount=Sum('Amount'))['sum_amount']
    avg_amount = data.aggregate(avg_amount=Avg('Amount'))['avg_amount']

    sum_amount = sum_amount if sum_amount else 0
    avg_amount = round(avg_amount, 2) if avg_amount else 0

    return render(request, 'admin/expences.html', {'data': data, 'current_month': current_month, 'sum': sum_amount, 'avg': avg_amount})


def returns(request):
    if request.session.get('user_role') == 'admin':
        filter = request.GET.get('filter')
        data = models.Returns.objects.all()
        if filter is not None and filter != 'all':
            data = data.filter(Staff = filter)

        staffs = models.Staffs.objects.all()
    else:
        data = models.Returns.objects.filter(Staff = request.session.get('user_id'))
        staffs = models.Staffs.objects.filter(id = request.session.get('user_id'))
    if request.method == 'POST':
        db = models.Returns()
        db.Staff = models.Staffs.objects.get(id=request.POST.get('staff'))
        db.Description = request.POST.get('description')
        db.Date = datetime.now()
        db.save()
        return redirect('return')
    return render(request, 'admin/returns.html', {'staffs': staffs, 'data': data,})


def editStaff(request, id):
    db = models.Staffs.objects.get(id = id)
    if request.method == 'POST':
        db.firstName = request.POST.get('firstName')
        db.lastName = request.POST.get('lastName')
        db.email = request.POST.get('email')
        db.phoneNumber = request.POST.get('phone')
        db.address = request.POST.get('address')
        db.gender = request.POST.get('gender')
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
