# Resultado de Aprendizaje: Arquitectura en Capas y Patrones de Diseno

## Arquitectura del proyecto

El proyecto combina la arquitectura MVT de Django con una arquitectura en capas.
La peticion HTTP entra por las rutas, pasa a la vista que funciona como fachada,
continua a la capa de servicios donde se encuentra la logica de negocio y finalmente
consulta los modelos que representan la base de datos.

```text
Cliente con JWT
      |
      v
products/urls.py
      |
      v
products/views.py          Facade
      |
      v
products/services.py       Strategy y logica de negocio
      |
      v
products/models.py         Factory Method y acceso a MariaDB
      |
      v
Respuesta JSON
```

## Tabla de patrones

| Patron | Categoria | Evidencia | Explicacion |
|---|---|---|---|
| Factory Method | Creacional | Metodo `Product.crear_con_categoria_default` en `products/models.py` | Centraliza la creacion de un producto. Si no se proporciona una categoria, obtiene o crea `Sin categoria` y la asigna automaticamente. |
| Strategy | Comportamiento | Clases de descuento y funcion `obtener_estrategia` en `products/services.py` | Encapsula distintos algoritmos de descuento y permite seleccionar uno segun la categoria sin llenar la vista de condiciones. Electronica aplica 10 %, Ropa 20 % y las demas no reciben descuento. |
| Facade | Estructural | Funcion `precio_final` en `products/views.py` | Presenta una sola operacion REST que oculta la consulta del producto, la seleccion de la estrategia y el calculo del precio final. El cliente solo necesita hacer una peticion GET. |

## Evidencia esperada del endpoint

```text
Electronica: 15000.00 -> 13500.00 (10 % de descuento)
Ropa:          1000.00 ->   800.00 (20 % de descuento)
Sin token: HTTP 401 Unauthorized
```

## Conclusion

Se agrego una capa de servicios al proyecto Django REST y se implementaron los
patrones Factory Method, Strategy y Facade. El endpoint protegido con JWT calcula
el descuento correspondiente a cada categoria. Las ocho pruebas unitarias terminan
correctamente: las seis pruebas CRUD existentes y las dos pruebas nuevas del endpoint.

