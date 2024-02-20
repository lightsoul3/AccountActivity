from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseForbidden
from .models import Good, Category
from .forms import CategoryForm, GoodForm, SearchForm, RegistrationForm, LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def can_modify_object(user, obj):
    return user.is_authenticated and obj.creator == user

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Assuming password1 is the password field
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return HttpResponseRedirect(reverse('get_goods'))  # Redirect to home page after successful login
    else:
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def login_user(request):
    error_message = None  # Initialize error message as None
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('get_goods')  # Redirect to home page after login
            else:
                error_message = "Invalid username or password."  # Invalid login credentials
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form, 'error_message': error_message})


def logout_user(request):
    return logout(request)

@login_required(login_url='login_user')
#view of home page with list of all goods and search of goods by name
def get_goods(request):
    if request.method == 'GET':
        goods = Good.objects.all()
        form = SearchForm()
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            goods = Good.objects.filter(name__icontains=search_query)
        else:
            goods = Good.objects.all()
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

    return render(request, template_name='goods/goods.html', context={'goods': goods, 'form': form})

@login_required(login_url='login_user')
#view of one good item with mode details and full picture
def get_good(request, pk=None):
    if request.method == 'GET':
        good = Good.objects.get(pk=pk)
        return render(request, template_name='goods/good.html', context={'good': good})
    return HttpResponseNotAllowed(["GET"])

@login_required(login_url='login_user')
#view of editing good item
def update_good(request, pk=None):
    obj = get_object_or_404(Good, pk=pk)
    good = Good.objects.get(pk=pk)

    # Check if the current user has permission to modify the object
    if not can_modify_object(request.user, obj):
        return HttpResponseForbidden("You don't have permission to modify this object.")
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            good.save()
            return HttpResponseRedirect(reverse('get_goods'))
    else:
        form = GoodForm(instance=good)
    return render(request, 'goods/update_good.html', {'form': form})

@login_required(login_url='login_user')
#view of delete good item 
def delete_good(request, pk=None):
    if request.method == 'GET':
        Good.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('get_goods'))
    return HttpResponseNotAllowed(["GET"])

@login_required(login_url='login_user')
#view of creating new good item 
def create_good(request):
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES)
        if form.is_valid():
            good = form.save(commit=False)
            good.creator = request.user  # Set the creator to the current logged-in user
            good.save()
            return HttpResponseRedirect(reverse('get_goods'))
    else:
        form = GoodForm()
    return render(request, 'goods/create_good.html', {'form': form})

@login_required(login_url='login_user')
#view of page with list of all categories and search of categories by name
def get_categories(request):
    #Categories Page
    if request.method == 'GET':
        categories = Category.objects.all()
        form = SearchForm() 
        return render(request, template_name='categories/categories.html', context={'categories': categories, 'form': form})
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            categories = Category.objects.filter(name__icontains=search_query)
        else:
            categories = Category.objects.all()
        return render(request, template_name='categories/categories.html', context={'categories': categories, 'form': form})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

@login_required(login_url='login_user')
#view of one category 
def get_category(request, pk=None):
    if request.method == 'GET':
        category = Category.objects.get(pk=pk)
        return render(request, template_name='categories/category.html', context={'category': category}) 
    return HttpResponseNotAllowed(["GET"])

@login_required(login_url='login_user')
#view of edit for category
def update_category(request, pk=None):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('get_categories'))
    else: 
        form = CategoryForm(instance=category)  
    return render(request, 'categories/update_category.html', {'form': form})

@login_required(login_url='login_user')
#view of dekete category
def delete_category(request, pk=None):
    if request.method == 'GET':
        Category.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('get_categories'))
    return HttpResponseNotAllowed(["GET"])

@login_required(login_url='login_user')
#view of craeting new one category
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.creator = request.user 
            form.save()
            return HttpResponseRedirect(reverse('get_categories'))
    else:
        form = CategoryForm()
    return render(request, template_name='categories/create_category.html', context={'form': form})

