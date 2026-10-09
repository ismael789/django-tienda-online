from decimal import Decimal
import unicodedata

from django.shortcuts import get_object_or_404

from .models import Product


class EstrategiaDescuento:
    """Interfaz comun para las estrategias de descuento."""

    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return Decimal(precio) * Decimal('0.90')


class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return Decimal(precio) * Decimal('0.80')


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return Decimal(precio)


def obtener_estrategia(categoria_nombre):
    estrategias = {
        'electronica': DescuentoElectronica(),
        'ropa': DescuentoRopa(),
    }
    nombre_normalizado = ''.join(
        caracter
        for caracter in unicodedata.normalize('NFD', categoria_nombre)
        if unicodedata.category(caracter) != 'Mn'
    ).casefold()
    return estrategias.get(nombre_normalizado, SinDescuento())


def calcular_precio_final(producto_id):
    """Coordina la consulta del producto y la estrategia de descuento."""
    producto = get_object_or_404(Product, pk=producto_id)
    estrategia = obtener_estrategia(producto.category.name)
    precio_con_descuento = estrategia.calcular(producto.price)

    return {
        'producto': producto.name,
        'categoria': producto.category.name,
        'precio_original': producto.price,
        'precio_final': round(precio_con_descuento, 2),
    }
