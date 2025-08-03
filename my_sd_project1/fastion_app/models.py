from django.db import models
from django.contrib.auth.models import User

# ---------------- SignupData Model ----------------
class SignupData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)     
    country_code = models.CharField(max_length=10)              

    def _str_(self):  
        return f"{self.user.username}'s Profile"

# ---------------- CartItem Model ----------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_image = models.URLField()
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def total_price(self):
        return self.quantity * self.price

    def _str_(self):  
        return f"{self.product_name} - {self.quantity}pcs"

# ---------------- Choices ----------------
PAYMENT_CHOICES = [
    ('Card', 'Card'),
    ('bKash', 'bKash'),
    ('Nagad', 'Nagad'),
    ('COD', 'Cash on Delivery'),
]

ORDER_STATUS = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
]

# ---------------- Order Model ----------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    country = models.CharField(max_length=50)                  # e.g., Bangladesh
    country_code = models.CharField(max_length=10)             # e.g., +88
    ordered_products = models.TextField()                      # JSON string or formatted
    total_price = models.FloatField()                          # total without delivery
    delivery_charge = models.FloatField()
    combined_total = models.FloatField()                       # total_price + delivery
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):  # ✅ Fixed method name
        return f"Order #{self.id} by {self.user.username}"