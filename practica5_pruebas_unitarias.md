# Unidad 1 - Practica 5: Pruebas Unitarias en Django

## Objetivo

Comprobar automaticamente las operaciones principales de la API de productos y categorias: crear, listar, actualizar y eliminar. Como los endpoints usan JWT, las pruebas autentican al usuario de prueba con `force_authenticate`.

## Paso 1. Activar el entorno virtual

Abrir PowerShell en la carpeta del proyecto y ejecutar:

```powershell
cd "C:\Users\ismae\OneDrive\Desktop\RespaldoMongo\django-project"
.\venv\Scripts\Activate.ps1
```

La activacion del entorno virtual es un paso de ejecucion, pero no es una captura obligatoria del entregable.

## Paso 2. Revisar las pruebas

El archivo que contiene las pruebas es [products/tests.py](products/tests.py). Incluye seis pruebas:

1. `test_create_category`: crea una categoria mediante `POST` y verifica que la API responda `201 Created` y guarde dos categorias.
2. `test_list_categories`: consulta las categorias mediante `GET` y verifica que la API responda `200 OK` con la categoria inicial.
3. `test_create_product`: crea un producto con una categoria existente y verifica que la API responda `201 Created`.
4. `test_list_products`: consulta los productos mediante `GET` y verifica que la API responda `200 OK` y devuelva un producto.
5. `test_update_product`: modifica los datos de un producto y verifica que la API responda `200 OK` y guarde el nuevo nombre.
6. `test_delete_product`: elimina un producto y verifica que la API responda `204 No Content` y que no queden productos.

Cada clase crea un usuario de prueba y ejecuta `force_authenticate`, por lo que las pruebas funcionan aunque las vistas tengan `permission_classes = [IsAuthenticated]`.

### Captura obligatoria 1: archivo `tests.py`

Tomar una captura de [products/tests.py](products/tests.py). La captura debe mostrar, en la medida de lo posible:

- Los imports de `TestCase`, `User`, `APIClient`, `Category` y `Product`.
- El metodo `setUp` de cada clase.
- Las seis funciones cuyos nombres empiezan con `test_`.
- Las comprobaciones `assertEqual` de los estados `201`, `200` y `204`.

Si el archivo no cabe completo en una sola pantalla, se pueden tomar varias capturas del mismo archivo y colocarlas juntas en el PDF bajo el titulo **Captura 1: tests.py**.

### Codigo que debe aparecer en la captura 1

```python
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Category, Product


class CategoryTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(
			username='test_user',
			password='test_password123',
		)
		self.client.force_authenticate(user=self.user)
		self.category = Category.objects.create(name='Electronica')

	def test_create_category(self):
		response = self.client.post('/api/categories/', {'name': 'Ropa'})
		self.assertEqual(response.status_code, 201)
		self.assertEqual(Category.objects.count(), 2)

	def test_list_categories(self):
		response = self.client.get('/api/categories/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)


class ProductTestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(
			username='test_user',
			password='test_password123',
		)
		self.client.force_authenticate(user=self.user)
		self.category = Category.objects.create(name='Electronica')
		self.product = Product.objects.create(
			name='Laptop',
			category=self.category,
			description='Laptop HP',
			price=15000.00,
		)

	def test_create_product(self):
		response = self.client.post('/api/products/', {
			'name': 'Mouse',
			'category': self.category.id,
			'description': 'Mouse inalambrico',
			'price': 500.00,
		})
		self.assertEqual(response.status_code, 201)
		self.assertEqual(Product.objects.count(), 2)

	def test_list_products(self):
		response = self.client.get('/api/products/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)

	def test_update_product(self):
		response = self.client.put(
			f'/api/products/{self.product.id}/',
			{
				'name': 'Laptop Pro',
				'category': self.category.id,
				'description': 'Laptop HP actualizada',
				'price': 18000.00,
			},
		)
		self.assertEqual(response.status_code, 200)
		self.product.refresh_from_db()
		self.assertEqual(self.product.name, 'Laptop Pro')

	def test_delete_product(self):
		response = self.client.delete(f'/api/products/{self.product.id}/')
		self.assertEqual(response.status_code, 204)
		self.assertEqual(Product.objects.count(), 0)
```

## Paso 3. Ejecutar las pruebas

Con el entorno virtual activado, ejecutar:

```powershell
python manage.py test
```

Tambien se puede ejecutar solamente la app:

```powershell
python manage.py test products
```

La salida esperada debe incluir:

```text
Found 6 test(s).
......
----------------------------------------------------------------------
Ran 6 tests in aproximadamente 1 segundo

OK
```

### Captura obligatoria 2: resultado de las pruebas

Tomar una captura de la terminal despues de ejecutar `python manage.py test`. La captura debe mostrar:

- El comando `python manage.py test`.
- `Found 6 test(s).`
- Los seis puntos: `......`.
- `Ran 6 tests`.
- `OK`.

No es necesario que la captura muestre los avisos de MariaDB o `DEFAULT_AUTO_FIELD`; lo importante es que se vean las seis pruebas ejecutadas y el resultado `OK`.

### Texto que debe aparecer en la captura 2

```text
PS C:\Users\ismae\OneDrive\Desktop\RespaldoMongo\django-project> python manage.py test
Found 6 test(s).
......
----------------------------------------------------------------------
Ran 6 tests in 1.291s

OK
Destroying test database for alias 'default'...
```

## Paso 4. Funcionamiento de JWT en las pruebas

No se copia un token manualmente en cada prueba. Esta linea simula un usuario autenticado para el cliente de pruebas:

```python
self.client.force_authenticate(user=self.user)
```

Esto permite verificar el comportamiento de los endpoints protegidos sin generar tokens reales durante cada prueba. En la aplicacion funcionando, el flujo JWT continua siendo:

1. Obtener un token en `/api/token/`.
2. Enviar el access token como `Authorization: Bearer <token>`.
3. Acceder a `/api/products/` o `/api/categories/`.

La evidencia de JWT no es una captura obligatoria para esta practica. Solo debe incluirse si el docente solicita demostrar tambien la autenticacion de la practica anterior.

## Paso 5. Preparar el PDF

El PDF debe contener, en este orden:

1. Portada con el nombre de la practica y los datos del alumno.
2. **Captura 1:** archivo `products/tests.py` con las seis pruebas escritas.
3. Breve explicacion de cada prueba, de 1 o 2 lineas.
4. **Captura 2:** terminal con `python manage.py test`, las seis pruebas pasando y `OK`.
5. Una breve conclusion: las seis pruebas terminaron correctamente.

El entregable es **un solo PDF**. No es necesario entregar un PDF separado por cada captura.

## Resultado verificado

En este proyecto se ejecuto:

```powershell
python manage.py test products
```

Resultado obtenido:

```text
Found 6 test(s).
......
----------------------------------------------------------------------
Ran 6 tests in 1.270s

OK
```

Django mostro advertencias sobre `MariaDB Strict Mode` y `DEFAULT_AUTO_FIELD`, pero no son fallos de las pruebas: las seis pruebas terminaron correctamente.
