# Evidencia de los Pasos Realizados

A continuación, te muestro los fragmentos de código de cada uno de los archivos modificados. Esto te servirá como "foto" o evidencia de que cada paso está implementado.

### 1. Modificar `models.py`
Se agregó el modelo `Category` y la relación `ForeignKey` en `Product`.

```python
# products/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='get_products',
        verbose_name='Categoria'
    )
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    is_active = models.BooleanField(default=True)
    # ...
```

### 2. Modificar `admin.py`
Se registró el modelo `Category` para que aparezca en el panel de administración.

```python
# products/admin.py
from django.contrib import admin
from .models import Product, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
```

### 3. Modificar `serializers.py`
Se agregó el `CategorySerializer`.

```python
# products/serializers.py
from rest_framework import serializers
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
```

### 4. Modificar `views.py`
Se agregó el `CategoryViewSet`.

```python
# products/views.py
from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
```

### 5. Modificar `urls.py`
Se registró la ruta de `categories` en el router.

```python
# products/urls.py
from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))
]
```

### 6. Crear las migraciones en la terminal
Al ejecutar los comandos de migración con tu entorno virtual, este es el resultado en la consola, que confirma que la base de datos ya está actualizada:

```powershell
PS C:\Users\ismae\OneDrive\Desktop\RespaldoMongo\django-project> python manage.py makemigrations
No changes detected

PS C:\Users\ismae\OneDrive\Desktop\RespaldoMongo\django-project> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, products, sessions
Running migrations:
  No migrations to apply.
```
