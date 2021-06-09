from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import MyCreateUserForm, ProductForm
from django.contrib.auth import authenticate, login as login_in, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account, Order, Product
from django.urls import reverse
from .decorators import unauthenticated_user, allowed_users


@unauthenticated_user
def login(request):

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


@unauthenticated_user
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
@allowed_users(allowed_roles=['customer'])
def main(request):

    products = Product.objects.exclude(date_added='2021-06-09')
    product1 = Product.objects.get(pk=1)
    product2 = Product.objects.get(pk=2)
    product3 = Product.objects.get(pk=3)
    product4 = Product.objects.get(pk=4)
    product5 = Product.objects.get(pk=5)

    # "products" content of context dictionary must be available, in order to show the "display" key
    context = {
        "products": products,
        "display1": product1,  # just for display, need storage to keep image files stay
        "display2": product2,
        "display3": product3,
        "display4": product4,
        "display5": product5,
    }

    return render(request, 'chickstore/mainpage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def edit_profile(request, customer_id):

    customer = Account.objects.filter(pk=customer_id)
    context = {
        'customer': customer
    }

    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        Account.objects.filter(pk=customer_id).update(
            phone=phone, address=address)

        messages.success(request, 'Profile is successfully edited.')

        return redirect(reverse('mainpage'))

    return render(request, 'account/edit-profile.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def orders(request, customer):
    orders = Order.objects.filter(customer=customer)

    context = {
        "orders": orders
    }

    return render(request, 'chickstore/orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def delete_order(request, order_id):

    current_user = request.user
    Order.objects.get(pk=order_id).delete()

    return redirect(reverse('orders', kwargs={'customer': int(current_user.id)}))


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
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


@login_required(login_url='login')
def about(request):
    return render(request, 'chickstore/about.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def staff_page(request):

    pending_orders = Order.objects.filter(status='Pending')
    delivered_orders = Order.objects.filter(status='In Delivery')

    products = Product.objects.all()
    customers = Account.objects.filter(group=1)

    context = {
        'pending': pending_orders,
        'delivered': delivered_orders,
        'products': products,
        'customers': customers
    }

    return render(request, 'chickstore/staff.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def deliver(request, order_id):

    Order.objects.filter(pk=order_id).update(status='In Delivery')

    return redirect('staff_page')


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def cancel_delivery(request, order_id):

    Order.objects.filter(pk=order_id).update(status='Pending')

    return redirect('staff_page')


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def add_product(request):

    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('staff_page')

    context = {
        'form': form
    }

    return render(request, 'chickstore/addproduct.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def edit_product(request, product_id):

    product = Product.objects.get(pk=product_id)
    context = {
        'preName': product.name,
        'prePrice': product.price,
        'preExtra': product.extra
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        extra = request.POST.get('extra')

        Product.objects.filter(pk=product_id).update(
            name=name, price=price, extra=extra)

        messages.success(request, 'Product has been successfully edited!')

        return redirect(reverse('edit_product', kwargs={'product_id': product_id}))

    else:
        return render(request, 'chickstore/editproduct.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def delete_product(request, product_id):

    name = Product.objects.get(pk=product_id).name
    Product.objects.filter(pk=product_id).delete()
    messages.success(request, name+' is successfully deleted.')

    return redirect(reverse('staff_page'))
