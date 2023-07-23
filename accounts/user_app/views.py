from collections import defaultdict
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
import calendar

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
    sales_not_added = True
    current_month = datetime.now().month
    month = request.GET.get('month')
    if month:
        current_month = month

    if request.session.get('user_role') == 'admin':
        staff = request.GET.get('staff')
        print(staff)
        if staff:
            sales = models.Sales.objects.filter(Staff__id = int(staff), Date__month = current_month).order_by('Date')
            print('fa')
        else:
            sales = models.Sales.objects.filter(Date__month = current_month).order_by('Date')
    else:
        sales = models.Sales.objects.filter(Staff__id = request.session.get('user_id'), Date__month = current_month).order_by('Date')
    current_day = datetime.now().date
    products = models.Products.objects.all()
    staffs = models.Staffs.objects.all()

    filteredSales = filterSales(sales)
    print(filteredSales, type(filteredSales))
    card_info = getSummary(filteredSales, current_month)

    if (sales.filter(Date = datetime.now().strftime("%Y-%m-%d")).exists()) :
        sales_not_added = False

    print(current_month, type(current_month))
    current_month_full = calendar.month_name[int(current_month)]


    if request.method == 'POST':
        values = dict(request.POST.items())
        for product in products:
            db = models.Sales()
            db.Date = values['date']
            db.Product = product
            db.NumberOfSales = values[product.name]
            db.Discount = int(request.POST.get('discount'))
            db.Staff = models.Staffs.objects.get(id = values['staff'])
            db.save()

        return redirect('admin_home')

    return render(request, 'admin/home.html', {'products': products, 'staffs': staffs, 'sales': filteredSales, 'current_day': current_day, "sales_added": sales_not_added, 'current_month': current_month, 'current_month_full': current_month_full, 'card_data': card_info})


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
        db.Date = (request.POST.get('date')).isoformat()
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

    data = data.order_by('Date')
    
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


def editExpence(request, id):
    db = models.Expences.objects.get(id = id)
    db.Date = request.POST.get('date')
    db.Purchase = request.POST.get('purchase')
    db.Remark = request.POST.get('remark')
    db.Amount = request.POST.get('amount')
    db.save()
    return redirect('expences')


def editReturn(request, id):
    db = models.Returns.objects.get(id=id)
    db.Staff = models.Staffs.objects.get(id = request.POST.get('staff'))
    db.Description = request.POST.get('description')
    db.save()
    return redirect('return')


def toggleActive(request):
    staff = models.Staffs.objects.get(id = request.GET.get('id'))
    if (request.GET.get('status') == 'true'):
        value = True
    else:
        value = False
    staff.status = value
    staff.save()

    return redirect('staffs')

def toggleAccess(request):
    staff = models.Staffs.objects.get(id = request.GET.get('id'))
    if (request.GET.get('status') == 'true'):
        value = True
    else:
        value = False
    staff.access = value
    staff.save()

    return redirect('staffs')


def addProduct(request):
    db = models.Products()
    db.name = request.POST.get('name')
    db.sellingPrice = int(request.POST.get('selling_price'))
    db.purchacePrice = int(request.POST.get('purchace_price'))
    db.vendor = request.POST.get('vendor')
    db.save()

    return redirect('admin_home')




def filterSales(data):
    if(len(data) == 0):
        return ''
    output = []
    values = {'totalNumberProducts': 0, 'totalSale_rs': 0, 'profit': 0}
    for index, sales in enumerate(data):
        if index == 0:
            values['date'] = sales.Date.isoformat()
            values[sales.Product.id] = sales.NumberOfSales
            values['totalNumberProducts'] = values[sales.Product.id]
            values['totalSale_rs'] = sales.Total + values['totalSale_rs']
            values['profit'] = sales.Profit + values['profit']
        else:
            if sales.Date.isoformat() != values['date']:
                values['profit'] = values['profit'] - 2000
                output.append(values)
                values = {'totalNumberProducts': 0, 'totalSale_rs': 0, 'profit': 0}
                values['date'] = sales.Date.isoformat()
                if sales.Product.id in values:
                    values[sales.Product.id] = values[sales.Product.name] + sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']
                else:
                    values[sales.Product.id] = sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']                
                values['totalSale_rs'] = sales.Total + values['totalSale_rs']
                values['profit'] = sales.Profit + values['profit']

            else:
                if sales.Product.id in values:
                    values[sales.Product.id] = values[sales.Product.id] + sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']
                else:
                    values[sales.Product.id] = sales.NumberOfSales
                    values['totalNumberProducts'] = sales.NumberOfSales + values['totalNumberProducts']
                values['profit'] = sales.Profit + values['profit']
                values['totalSale_rs'] = sales.Total + values['totalSale_rs']

    
    values['profit'] = values['profit'] - 2000
    output.append(values)

    print(output)

    return output


def getSummary(data, month):
    summary = {'total_psc': 0, 'total_expence': 0, 'total_profit': 0, 'total_income': 0}
    expences = models.Expences.objects.filter(Date__month = month)
    total = expences.aggregate(Sum('Amount'))
    if (total['Amount__sum']) is None:
        summary['total_expence'] = 0
    else:
        summary['total_expence'] = total['Amount__sum']

    for i in data:
        summary['total_income'] = summary['total_income'] + i['totalSale_rs']
        summary['total_profit'] = summary['total_profit'] + i['profit']
        summary['total_psc'] = summary['total_psc'] + i['totalNumberProducts']
    
    summary['total_profit'] = summary['total_profit'] - summary['total_expence']
    print(summary)
    return summary