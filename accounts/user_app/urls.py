from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('staffs', views.staffs, name='staffs'),
    path('add_staff', views.add_staff, name='add-staffs'),
    path('expences', views.expences, name='expences'),
    path('returns', views.returns, name='return'),
    path('edit-staff-<id>', views.editStaff, name='edit_staff'),
    path('edit_expence-<id>', views.editExpence, name='edit-expences'),
    path('edit-return-<id>', views.editReturn, name='edit-return'),
    path('toggle-active-status/', views.toggleActive, name='toggle-active'),
    path('toggle-access-status/', views.toggleAccess, name='toggle-access'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)