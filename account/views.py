from django.shortcuts import get_object_or_404, render, redirect
from .forms import MyCreateUserForm
from django.contrib.auth import authenticate, login as login_in, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, Product
from django.urls import reverse
from django.views.generic import DetailView


def login(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login_in(request, user)
                return redirect('mainpage')

            else:
                messages.error(request, 'Invalid credentials')

    return render(request, 'account/login.html')


def register(request):
    form = MyCreateUserForm()

    if request.method == "POST":
        form = MyCreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+username)

            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'account/signup.html', context)


def logoutView(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def main(request):

    products = Product.objects.exclude(pk=1)
    product = Product.objects.get(pk=1)

    context = {
        "products": products,
        "display": product,  # just for display, need storage to keep image files stay
    }

    return render(request, 'chickstore/mainpage.html', context)


@login_required(login_url='login')
def orders(request, customer):
    orders = Order.objects.filter(customer=customer)

    context = {
        "orders": orders
    }

    return render(request, 'chickstore/orders.html', context)


@login_required(login_url='login')
def productpage(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    current_user = request.user

    context = {
        'product': product
    }

    if request.method == "POST":
        amount = request.POST.get("amount")
        total_price = product.price * int(amount)

        order = Order(customer=current_user,
                      product=product, quantity=amount, price_sum=total_price, status="Pending")
        order.save()

        return redirect(reverse('orders', kwargs={'customer': int(current_user.id)}))

    return render(request, 'chickstore/productpage.html', context)


# class ProductImage(DetailView):
#     model = Product
#     context_object_name = 'product'
