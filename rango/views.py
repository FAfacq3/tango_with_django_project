from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from rango.models import Category, Page

from django.shortcuts import render
from rango.models import Category, Page
from datetime import datetime
import logging

def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]

    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits

    response = render(request, 'rango/index.html', {
        'categories': categories,
        'pages': pages,
        'visits': visits
    })

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    try:
        last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        last_visit_time = datetime.now()

    if (datetime.now() - last_visit_time).days > 0:
        request.session['visits'] = visits + 1
        response.set_cookie('last_visit', str(datetime.now()))

    return response

def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    pages = Page.objects.filter(category=category).order_by('-views')

    return render(request, 'rango/category.html', {'category': category, 'pages': pages})

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

def add_page(request, category_name):
    category = get_object_or_404(Category, name=category_name)

    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect('rango:show_category', category_name=category.name)
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rango")


def show_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    page.views += 1
    page.save()

    logger.info(f"Page '{page.title}' visited, now has {page.views} views")
    print(f"Page '{page.title}' visited, now has {page.views} views")

    return redirect(page.url)

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
            return redirect('rango:index')
        else:
            return render(request, 'rango/login.html', {'error': 'Invalid username or password'})

    return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('rango:index')

@require_POST
@csrf_exempt
def like_category(request):
    category_id = request.POST.get("category_id")

    if not category_id:
        return JsonResponse({"status": "error", "message": "No category ID provided"}, status=400)

    try:
        category = Category.objects.get(id=category_id)
        category.likes += 1
        category.save()
        return JsonResponse({"status": "ok", "likes": category.likes})
    except Category.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Category not found"}, status=404)

def search(request):
    query = request.GET.get("query", "")

    if query:
        pages = Page.objects.filter(title__icontains=query)[:5]
        results = [{"title": page.title, "url": page.url} for page in pages]
        return JsonResponse({"pages": results})

    return JsonResponse({"pages": []})
