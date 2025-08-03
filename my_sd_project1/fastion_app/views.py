from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import SignupData
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order
from django.shortcuts import redirect, get_object_or_404
import re
from django.http import HttpResponse



def get_country_name(code):
    return {
        "BD": "Bangladesh",
        "IN": "India",
        "PAK": "Pakistan",
        "UK": "United Kingdom",
        "Others": "Others"
    }.get(code, "Unknown")


DELIVERY_CHARGES = {
    "BD": 60,
    "IN": 120,
    "UK": 250,
    "PAK": 180,
    "Others": 350,
}






def home(request):
    return render(request, 'fastion_app/home.html')

def onepiece(request):
    return render(request, 'fastion_app/onepiece.html')

def salwarkameez(request):
    return render(request, 'fastion_app/salwarkameez.html')

def saree(request):
    return render(request, 'fastion_app/saree.html')

def babyboy(request):
    return render(request, 'fastion_app/babyboy.html')

def babygirl(request):
    return render(request, 'fastion_app/babygirl.html')

def accessories(request):
    return render(request, 'fastion_app/accessories.html')

def groom(request):
    return render(request, 'fastion_app/groom.html')

def bride(request):
    return render(request, 'fastion_app/bride.html')

def shoes(request):
    return render(request, 'fastion_app/shoes.html')

def bag(request):
    return render(request, 'fastion_app/bag.html')

def men1(request):
    return render(request, 'fastion_app/men1.html')

def aboutUs(request):
    return render(request, 'fastion_app/aboutUs.html')

def sale(request):
    return render(request, 'fastion_app/sale.html')

def terms(request):
    return render(request, 'fastion_app/terms.html')

def career(request):
    return render(request, 'fastion_app/career.html')

def professionalJobs(request):
    return render(request, 'fastion_app/professionalJobs.html')

def services(request):
    return render(request, 'fastion_app/services.html')

def cookie(request):
    return render(request, 'fastion_app/cookie.html')

def myCart(request):
    return render(request, 'fastion_app/myCart.html')

def professionalIntern(request):
    return render(request, 'fastion_app/professionalIntern.html')

def appointment(request):
    return render(request, 'fastion_app/appointment.html')

def privacy(request):
    return render(request, 'fastion_app/privacy.html')

def contactUs(request):
    return render(request, 'fastion_app/contactUs.html')

def code(request):
    return render(request, 'fastion_app/code.html')

def faq(request):
    return render(request, 'fastion_app/faq.html')

def locations(request):
    return render(request, 'fastion_app/locations.html')

def jobapply(request):
    return render(request, 'fastion_app/jobapply.html')

def license(request):
    return render(request, 'fastion_app/license.html')

def payment_view(request):
    # your logic here
    return render(request, 'fastion_app/payment.html')

# Signup
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        country = request.POST.get('country', '')         # ✅ ADD THIS
        country_code = request.POST.get('countryCode')
        address = request.POST['address']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        SignupData.objects.create(
            user=user,
            phone_number=phone,
            address=address,
            country=country,                      # ✅ ADD THIS
            country_code=country_code
        )

        messages.success(request, "Account created! Please login.")
        return redirect('login')
    return render(request, 'fastion_app/signup.html')

# Login
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"{username}, let's get shopping! 🛍")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'fastion_app/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('home')

def myCart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('login')

    cart_items = CartItem.objects.filter(user=request.user)
    total_items = sum(item.quantity for item in cart_items)
    grand_total = sum(item.total_price() for item in cart_items)

    return render(request, 'fastion_app/myCart.html', {
        'cart_items': cart_items,
        'total_items': total_items,
        'grand_total': grand_total,
    })



@login_required
def myCart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    # total_items = CartItem.objects.filter(user=request.user).count()
    total_items = sum(item.quantity for item in cart_items)
    grand_total = sum(item.total_price() for item in cart_items)
    return render(request, 'fastion_app/myCart.html', {
        'cart_items': cart_items,
        'total_items': total_items,
        'grand_total': grand_total,
    })

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    cart_items = CartItem.objects.filter(user=request.user)
    total_items = sum(item.quantity for item in cart_items)
    return redirect('myCart')

@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        product_image = request.POST.get("product_image")
        size = request.POST.get("size")
        quantity = int(request.POST.get("quantity", 1))
        price = float(request.POST.get("price"))

        # Check if item already in cart, update quantity if so
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product_name=product_name,
            size=size,
            defaults={
                "product_image": product_image,
                "quantity": quantity,
                "price": price,
            }
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('myCart')
    return redirect('home')

@login_required
def payment_view(request):
    try:
        user_profile = SignupData.objects.get(user=request.user)
    except SignupData.DoesNotExist:
        messages.error(request, "Profile information missing!")
        return redirect('myCart')

    cart_items = CartItem.objects.filter(user=request.user)
    total_cart_amount = sum(item.total_price() for item in cart_items)

    user_country_code = user_profile.country_code
    delivery_charge = DELIVERY_CHARGES.get(user_country_code, DELIVERY_CHARGES['BD'])
    delivery_charge = DELIVERY_CHARGES.get(user_country_code, DELIVERY_CHARGES['IN'])
    delivery_charge = DELIVERY_CHARGES.get(user_country_code, DELIVERY_CHARGES['UK'])
    delivery_charge = DELIVERY_CHARGES.get(user_country_code, DELIVERY_CHARGES['Others'])

    total_amount = total_cart_amount + delivery_charge

    context = {
        'user_profile': user_profile,
        'username': request.user.username,
        'delivery_charge': delivery_charge,
        'total_cart_amount': total_cart_amount,
        'total_amount': total_amount,
        'cart_items': cart_items,
    }
    return render(request, 'fastion_app/payment.html', context)


@login_required
def payment_done(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        trxid = request.POST.get('trxid', '').strip()

        user = request.user
        profile = SignupData.objects.get(user=user)
        cart_items = CartItem.objects.filter(user=user)
        total_amount = sum(item.total_price() for item in cart_items)
        delivery_charge = DELIVERY_CHARGES.get(profile.country_code, DELIVERY_CHARGES['Others'])
        delivery_charge = DELIVERY_CHARGES.get(profile.country_code, DELIVERY_CHARGES['BD'])
        delivery_charge = DELIVERY_CHARGES.get(profile.country_code, DELIVERY_CHARGES['IN'])
        delivery_charge = DELIVERY_CHARGES.get(profile.country_code, DELIVERY_CHARGES['UK'])
        combined_total = total_amount + delivery_charge

        # Validate trxid
        if method == "bKash" and not re.match(r'^[A-Za-z0-9]{10}$', trxid):
            return HttpResponse("Invalid bKash Transaction ID")
        elif method == "Nagad" and not re.match(r'^[0-9]{11}$', trxid):
            return HttpResponse("Invalid Nagad Transaction ID")
        elif method == "Card" and not re.match(r'^[A-Za-z0-9]{12,18}$', trxid):
            return HttpResponse("Invalid Card Transaction ID")

        # Prepare product info string
        product_info = ""
        for item in cart_items:
            product_info += f"{item.product_name} (x{item.quantity})\n"

        # Get readable country name from code
        country_name = get_country_name(profile.country_code)

        # Save order to database
        Order.objects.create(
            user=user,
            phone_number=profile.phone_number,
            address=profile.address,
            country=country_name,
            country_code=profile.country_code,
            ordered_products=product_info.strip(),
            total_price=total_amount,
            delivery_charge=delivery_charge,
            combined_total=combined_total,
            payment_method=method,
            transaction_id=trxid if trxid else None,
            status='Pending'
        )

        # Clear cart
        cart_items.delete()

        return render(request, 'fastion_app/payment_receipt.html', {
            'method': method,
            'trxid': trxid,
            'total': combined_total,
        })

    return redirect('payment')