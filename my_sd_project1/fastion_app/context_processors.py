from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    else:
        count = 0
    return {'total_items': count}


# def cart_item_count(request):
#     if request.user.is_authenticated:
#         items = CartItem.objects.filter(user=request.user)
#         print("🛒 Cart Items Loaded:", items)  # 👈 Debug print
#         return {'total_items': sum(item.quantity for item in items)}
#     return {'total_items': 0}
