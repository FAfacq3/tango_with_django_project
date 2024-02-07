from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Category, Page
from django.template.defaultfilters import slugify
from django.shortcuts import render, redirect
from .forms import CategoryForm
from .forms import PageForm
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list,
                    'pages': page_list}

    response = render(request, 'rango/index.html', context=context_dict)
    visitor_cookie_handler(request, response)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    visitor_cookie_handler(request, response)
    return response


def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html')
    visitor_cookie_handler(request, response)
    return response


def my_view(request):
    context = {'message': 'This is a message passed from the view.'}
    return render(request, 'rango/template.html', context)


def greeting_view(request):
    context = {'greeting_message': 'Have a great day!'}
    return render(request, 'rango/greeting.html', context)


def show_categories(request):
    categories = Category.objects.all()
    content_dict = {'categories': categories}
    return render(request, 'rango/categories.html', content=content_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category).order_by('-views')

    context_dict = {
        'category': category,
        'pages': pages,
    }

    return render(request, 'rango/category.html', context=context_dict)


def category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category)
    context_dict = {'category': category, 'pages': pages}
    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def populate():
    python_cat = add_category('Python', views=128, likes=64)

    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/3/tutorial/",
             views=128)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')


def some_view(request):
    if request.user.is_authenticated:
        return HttpResponse("You are logged in.")
    else:
        return HttpResponse("You are not logged in.")


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Redirect the user to the homepage after logout.
    return redirect(reverse('rango:index'))


def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        response.set_cookie('last_visit', last_visit_cookie)

    request.session['visits'] = visits


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
