from itertools import product

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from women.forms import QuantityForm
from women.models import Category, Product


# Create your views here.
def index(request):
    catalog = Category.objects.all()
    data = {
        'titile': 'Главная страница',
        'catalog': catalog,
    }
    return render(request, 'women/index.html', data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О нас'})


def categories(request, cat_id):
    return HttpResponse("Hello, world. You're at the polls categories.")


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')


def category(request, slug):
    product = get_object_or_404(Category, slug=slug)
    related_products = Product.objects.filter(category_id=product.sub_category_id).all()[:5]
    context = {
        'title': product.title,
        'product': product,
        'favorites': 'favorites',
        'related_products': related_products
    }
    return render(request, 'women/catalog.html', context)


def product_detail(request, slug):
    form = QuantityForm()
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).all()[:5]
    context = {
        'title': product.title,
        'product': product,
        'form': form,
        'favorites': 'favorites',
        'related_products': related_products
    }
    return render(request, 'women/cat_detail.html', context)


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.likes.add(product)
    return redirect('women:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.likes.remove(product)
    return redirect('women:favorites')


@login_required
def favorites(request):
    products = request.user.likes.all()
    context = {'title': 'Favorites', 'products': products}
    return render(request, 'women/favorites.html', context)

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query).all()
    context = {'products': paginat(request, products)}
    return render(request, 'women/index.html', context)

def filter_by_category(request, slug):
    """when user clicks on parent category
    we want to show all products in its sub-categories too
    """
    result = []
    category = Category.objects.filter(slug=slug).first()
    [result.append(product) for product in Product.objects.filter(category=category.id).all()]
    # check if category is parent then get all sub-categories
    if not category.is_sub:
        sub_categories = category.sub_categories.all()
        # get all sub-categories products
        for category in sub_categories:
            [result.append(product)
             for product in Product.objects.filter(category=category).all()]
    context = {'products': paginat(request, result)}
    return render(request, 'women:index', context)
