from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    response = render(request, 'rango/index.html')

    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        response.set_cookie('visits', visits)
        response.set_cookie('last_visit', str(datetime.now()))

    response.context_data = {'visits': visits}  
    return render(request, 'rango/index.html', {'visits': visits})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            return redirect('login')
    else:
        user_form = UserForm()

    return render(request, 'rango/register.html', {'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'rango/login.html', {'error': 'Invalid username or password'})

    return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
