import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_online.settings')
django.setup()

from products.models import Category, Product

# Clear existing if any
Category.objects.all().delete()

# Create Categories
c1 = Category.objects.create(name="Electrónica")
c2 = Category.objects.create(name="Ropa")

# Create Products
Product.objects.create(
    name="Laptop",
    category=c1,
    description="Laptop gamer 16GB RAM",
    price=1200.00
)

Product.objects.create(
    name="Smartphone",
    category=c1,
    description="Smartphone 5G 128GB",
    price=600.00
)

Product.objects.create(
    name="Camiseta",
    category=c2,
    description="Camiseta de algodón talla M",
    price=15.00
)

print("Datos de prueba creados exitosamente.")
