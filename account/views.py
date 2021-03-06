from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import MyCreateUserForm, ProductForm, TagForm
from django.contrib.auth import authenticate, login as login_in, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account, Order, Product, Tag
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

    products = Product.objects.exclude(placeholder=True)
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
def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    product = Product.objects.get(pk=order.product.id)

    stock = order.quantity + product.quantity
    Product.objects.filter(pk=order.product.id).update(quantity=stock)

    current_user = request.user
    Order.objects.get(pk=order_id).delete()

    return redirect(reverse('orders', kwargs={'customer': int(current_user.id)}))

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

        if int(product.quantity) < int(amount):
            messages.info(request, 'Not enough stock.')
            return redirect(reverse('productpage', kwargs={'product_id':int(product_id)}))

        else:
            total_price = product.price * int(amount)
            order = Order(customer=current_user,
                        product=product, quantity=amount, price_sum=total_price, status="Pending")
            order.save()
            stock = int(product.quantity) - int(amount)
            Product.objects.filter(pk=product.id).update(quantity=stock)
            return redirect(reverse('orders', kwargs={'customer': int(current_user.id)}))

    return render(request, 'chickstore/productpage.html', context)


@login_required(login_url='login')
def about(request):
    return render(request, 'chickstore/about.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def staff_page(request):

    pending_orders = Order.objects.filter(status='Pending').order_by('-order_date')
    delivered_orders = Order.objects.filter(status='In Delivery').order_by('-order_date')

    products = Product.objects.all().order_by('id')
    customers = Account.objects.filter(group=1).order_by('id')

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
def tags(request):
    tags = Tag.objects.all()
    context = {
        'tags':tags
    }

    return render(request, 'chickstore/tags.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def add_tag(request):

    forms = TagForm()

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid:
            form.save()

            name = form.cleaned_data.get('name')    
            messages.success(request, name+' added!')
            return redirect('add_tag')

    context = {
        'form' : forms
    }
    return render(request, 'chickstore/addtag.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def delete_tag(request, tag_id):

    tag = Tag.objects.get(pk=tag_id)
    messages.success(request, 'Tag \''+ tag.name +'\' is deleted')
    Tag.objects.filter(pk=tag_id).delete()

    return redirect(reverse('manage_tags'))

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def edit_product(request, product_id):

    product = Product.objects.get(pk=product_id)
    tags = Tag.objects.order_by('id')
    context = {
        'preName': product.name,
        'prePrice': product.price,
        'preStock' : product.quantity,
        'preExtra': product.extra,
        'preTags' : product.tags.all(),
        'tags': tags
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        extra = request.POST.get('extra')
        quantity = request.POST.get('stock')
        selected_tags = request.POST.getlist('tags')

        #Insert selected id tag from template into product tag
        if selected_tags: 
            product.tags.clear() #REMOVE ALL TAG RELATIONS 
            for tag in selected_tags:
                product.tags.add(Tag.objects.get(id=tag))

            Product.objects.filter(pk=product_id).update(
                name=name, price=price, extra=extra, quantity=quantity)
            messages.success(request, 'Product has been successfully edited!')
            return redirect(reverse('edit_product', kwargs={'product_id': product_id}))
        else:        
            Product.objects.filter(pk=product_id).update(
                name=name, price=price, extra=extra, quantity=quantity)
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
