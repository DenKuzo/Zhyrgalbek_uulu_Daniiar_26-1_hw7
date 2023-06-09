from django.shortcuts import render, redirect
from products.models import Products, Review
from products.forms import ProductCreateForm, ReviewCreateForm
from products.constants import PAGINATION_LIMIT

# Create your views here.
def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Products.objects.all().order_by('-rate')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search:
            products = \
                products.filter(title__icontains=search) | products.filter(description__icontains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        max_page = round(max_page) +1 if round(max_page) < max_page else round(max_page)

        products = products[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]

        context = {
            'products': products,
            'user': request.user,
            'pages': range(1, max_page+1)
        }
        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Products.objects.get(id=id)

        context = {
            'product': product,
            'reviews': product.review_set.all(),
            'form': ReviewCreateForm
        }

        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        product = Products.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                product_id=id
            )

        context = {
            'product': product,
            'reviews': product.review_set.all(),
            'form': ReviewCreateForm
        }

        return render(request, 'products/detail.html', context=context)


def product_create_view(request):
    if request.method == 'GET':
        contex = {
            'form': ProductCreateForm

        }
        return render(request, 'products/create.html', context=contex)

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)

        if form.is_valid():
            Products.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate')
            )
            return redirect('/products/')

        return render(request, 'products/create.html', context={
            'form': form
        })
