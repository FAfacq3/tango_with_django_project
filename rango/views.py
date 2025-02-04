from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    categories = Category.objects.all()
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    response = render(request, 'rango/index.html', {'categories': categories, 'visits': visits})

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    try:
        last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        last_visit_time = datetime.now()
    if (datetime.now() - last_visit_time).days > 0:
        request.session['visits'] = visits + 1
        response.set_cookie('last_visit', str(datetime.now()))
    return response

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('index')
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

@csrf_exempt
def like_category(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        if category_id:
            try:
                category = Category.objects.get(id=int(category_id))
                category.likes += 1
                category.save()
                return JsonResponse({'status': 'ok', 'likes': category.likes})
            except Category.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Category not found'})
        return JsonResponse({'status': 'error', 'message': 'Invalid category_id'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})