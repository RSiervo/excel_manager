# accounts/urls.py
from django.urls import path
from .views import login_user, logout_user, register_user, dashboard, upload_excel, save_files, backup, restore # Import all views
from . import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('save_data/', views.save_data, name='save_data'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload_excel/', upload_excel, name='upload_excel'), 
    path('save_files/', save_files, name='save_files'),  
    path('backup/', backup, name='backup'),  
    path('restore/', restore, name='restore'), 
    path('services/', views.services, name='services'), 
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('load_excel_data/', views.load_excel_data, name='load_excel_data'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
