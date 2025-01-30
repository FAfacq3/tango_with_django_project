from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    categories = Category.objects.all()
    context_dict = {'categories': categories}
    return render(request, 'rango/index.html', context_dict)

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
