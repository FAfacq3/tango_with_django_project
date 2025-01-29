from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    categories = Category.objects.all()
    context_dict = {'categories': categories}
    return render(request, 'rango/index.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form})
