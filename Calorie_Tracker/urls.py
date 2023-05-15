from django.contrib import admin
from django.urls import path
from AuthApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('changepass/', views.user_change_pass, name='changepassword'),
    path('changepass1/', views.user_change_pass1, name='changepassword1'),
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_calorie_entry, name='add_calorie_entry'),
    path('edit/<int:pk>/', views.edit_calorie_entry, name='edit_calorie_entry'),
    path('delete/<int:pk>/', views.delete_calorie_entry, name='delete_calorie_entry'),
]
