from django.contrib import admin # type: ignore
from .models import CustomUser, Producto, Categoria, Carrito, Venta, VentaProducto, Estado
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(Venta)
admin.site.register(VentaProducto)
admin.site.register(Estado)
