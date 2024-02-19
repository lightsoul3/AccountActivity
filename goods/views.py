from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from .models import Good, Category
from .forms import CategoryForm, GoodForm, SearchForm
from django.urls import reverse

# Create your views here.

def login(request):
    pass

def logout(request):
    pass

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

def get_good(request, pk=None):
    if request.method == 'GET':
        good = Good.objects.get(pk=pk)
        return render(request, template_name='goods/good.html', context={'good': good})
    return HttpResponseNotAllowed(["GET"])

def update_good(request, pk=None):
    good = Good.objects.get(pk=pk)
    if request.method == 'POST':
        form = GoodForm(request.POST, request.FILES, instance=good)
        if form.is_valid():
            good.save()
            return HttpResponseRedirect(reverse('get_goods'))
    else:
        form = GoodForm(instance=good)
    return render(request, 'goods/update_good.html', {'form': form})

def delete_good(request, pk=None):
    if request.method == 'GET':
        Good.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('get_goods'))
    return HttpResponseNotAllowed(["GET"])

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


def get_category(request, pk=None):
    if request.method == 'GET':
        category = Category.objects.get(pk=pk)
        return render(request, template_name='categories/category.html', context={'category': category}) 
    return HttpResponseNotAllowed(["GET"])

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

def delete_category(request, pk=None):
    if request.method == 'GET':
        Category.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('get_categories'))
    return HttpResponseNotAllowed(["GET"])

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
          #  category = form.save(commit=False)
          #  category.creator = request.user 
            form.save()
            return HttpResponseRedirect(reverse('get_categories'))
    else:
        form = CategoryForm()
    return render(request, template_name='categories/create_category.html', context={'form': form})


