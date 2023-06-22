from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('staffs', views.staffs, name='staffs'),
    path('add_staff', views.add_staff, name='add-staffs'),
    path('expences', views.expences, name='expences'),
    path('returns', views.returns, name='return'),
]