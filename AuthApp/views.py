from django.utils import timezone
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, EditUserProfileForm, CalorieEntryForm, EditCaloriesForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from AuthApp.models import CalorieEntry
from django.db import models


# Signup view function
def sign_up(request):
    if not request.user.is_authenticated:
      if request.method == 'POST':
          fm = SignUpForm(request.POST)
          if fm.is_valid():
           messages.success(request, 'Account created successfully !!')
           fm.save()

      else:
        fm = SignUpForm()
      return render(request, 'AuthApp/signup.html', {'form':fm})
    else:
      return HttpResponseRedirect('/profile/') 
 
# Login view function
def log_in(request):
   if not request.user.is_authenticated:
      if request.method == 'POST':
        fm = AuthenticationForm(request=request, data = request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username = uname, password = upass)
            if user is not None:
              login(request, user)
              return HttpResponseRedirect('/profile/')
      else:
        fm = AuthenticationForm()
      return render(request, 'AuthApp/userLogin.html', {'form':fm})
   else:
      return HttpResponseRedirect('/profile/')

#Profile View   
def user_profile(request, ):
   if request.user.is_authenticated:
      if request.method == 'POST':
         fm = EditUserProfileForm(request.POST, instance = request.user)
         if fm.is_valid():
            messages.success(request, 'Profile Updated !!')
            fm.save()
      else:
         fm = EditUserProfileForm(instance = request.user)
      return render(request, 'AuthApp/profile.html', {'name': request.user, 'form':fm})
   else:
      return HttpResponseRedirect('/login/')


#Logout View
def user_logout(request):
   logout(request)
   return HttpResponseRedirect('/login/')


#Change Password with old passwords View
def user_change_pass(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
       fm = PasswordChangeForm(user=request.user, data=request.POST)
       if fm.is_valid():
         fm.save()
         update_session_auth_hash(request, fm.user)
         return HttpResponseRedirect('/profile/')
      else:
         fm = PasswordChangeForm(user = request.user)
      return render(request, 'AuthApp/changepassword.html', {'form':fm})
   
   else:
      return HttpResponseRedirect('/login/')

#Change passwords without old passwords

def user_change_pass1(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
       fm = SetPasswordForm(user=request.user, data=request.POST)
       if fm.is_valid():
         fm.save()
         update_session_auth_hash(request, fm.user)
         return HttpResponseRedirect('/profile/')
      else:
         fm = SetPasswordForm(user = request.user)
      return render(request, 'AuthApp/changepassword1.html', {'form':fm})
   
   else:
      return HttpResponseRedirect('/login/')
   

@login_required
def add_calorie_entry(request):
    if request.method == 'POST':
        form = CalorieEntryForm(request.POST)
        if form.is_valid():
            calorie_entry = form.save(commit=False)
            calorie_entry.user = request.user
            calorie_entry.save()
            return redirect('dashboard')
    else:
        form = CalorieEntryForm()
    return render(request, 'AuthApp/add_calorie_entry.html', {'form': form})

@login_required
def edit_calorie_entry(request, pk):
    calorie_entry = get_object_or_404(CalorieEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EditCaloriesForm(request.POST, instance=calorie_entry)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EditCaloriesForm(instance=calorie_entry)
    return render(request, 'AuthApp/edit_calorie_entry.html', {'form': form, 'calorie_entry': calorie_entry})


@login_required
def delete_calorie_entry(request, pk):
    calorie_entry = get_object_or_404(CalorieEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        calorie_entry.delete()
        return redirect('dashboard')
    return render(request, 'AuthApp/delete_calorie_entry.html', {'calorie_entry': calorie_entry})

@login_required
def dashboard(request):
    today = timezone.now().date()
    week_ago = today - timezone.timedelta(days=7)
    month_ago = today - timezone.timedelta(days=30)
    calorie_entries = CalorieEntry.objects.filter(user=request.user, date__gte=month_ago)
    calories_today = calorie_entries.filter(date=today).aggregate(models.Sum('calories'))['calories__sum'] or 0
    calories_this_week = calorie_entries.filter(date__gte=week_ago).aggregate(models.Sum('calories'))['calories__sum'] or 0
    calories_this_month = calorie_entries.aggregate(models.Sum('calories'))['calories__sum'] or 0
    context = {
        'calories_today': calories_today,
        'calories_this_week': calories_this_week,
        'calories_this_month': calories_this_month,
        'calorie_entries':calorie_entries,
    }
    return render(request, 'AuthApp/dashboard.html', context)