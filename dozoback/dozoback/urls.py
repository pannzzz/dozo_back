"""
URL configuration for dozoback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from Dozo import views
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from Dozo.views import ProductoListAPIView, ProductoDetailAPIView
from Dozo.views import CartView
from Dozo.views import RegisterUserView
from Dozo.views import PedidoDetailView
from Dozo.views import user_profile
from Dozo.views import productos_mas_vendidos
from Dozo.views import verify_current_password, change_password
from Dozo.views import logout_all_sessions
from Dozo.views import listar_pedidos_usuario
from Dozo.views import send_reset_password_email
from Dozo.views import reset_password


urlpatterns = [
    path('admin/', admin.site.urls),
    # User URLs
    path('users/registro/', views.registro, name='registro'),
    path('users/', views.mostrar_user, name='mostrar_user'),
    path('users/editar/<int:user_id>/', views.editar_user, name='editar_user'),
    path('users/eliminar/<int:user_id>/', views.eliminar_user, name='eliminar_user'),
    path('login/', views.loginzzz, name='login'),
    path('logout/', views.logout, name='logout'),
    path('api/logout-all/', logout_all_sessions, name='logout_all'),
    

    # Producto URLs
    path('productos/', views.mostrar_producto, name='mostrar_producto'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    # Categoria URLs
    path('categorias/', views.mostrar_categoria, name='mostrar_categoria'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Carrito URLs
    path('carritos/nuevo/', views.crear_carrito, name='crear_carrito'),
    path('cart/', CartView.as_view(), name='cart'),
    # Venta URLs
    path('ventas/editar/<int:venta_id>/', views.editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:venta_id>/', views.eliminar_venta, name='eliminar_venta'),
    path('api/ventas/', views.crear_venta_api, name='crear_venta_api'),
    path('ventas/', views.ventas_view, name='ventas'),
    
    #api
    path('api/productos/', ProductoListAPIView.as_view(), name='producto-list'),  # Nota el uso de .as_view()
    path('api/productos/<int:pk>/', ProductoDetailAPIView.as_view(), name='producto-detail'),
    path('api/pedidos/', views.listar_pedidos_usuario, name='listar_pedidos_usuario'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/products/', views.filter_products, name='filter_products'),
    path('api/pedidos/<int:id>/', PedidoDetailView.as_view(), name='pedido-detail'),
    path('api/user/profile/', user_profile, name='user_profile'),
    path('productos-mas-vendidos/', productos_mas_vendidos, name='productos_mas_vendidos'),
    path('api/user/profile/edit/', views.edit_user_profile, name='edit_user_profile'),
    path("api/verify-current-password/", verify_current_password, name="verify_current_password"),
    path("api/change-password/", change_password, name="change_password"),

    path('api/user/orders/', listar_pedidos_usuario, name='listar_pedidos_usuario'),
    path('api/reset-password/', send_reset_password_email, name='reset-password'),
    path('api/reset-password/<int:user_id>/', reset_password, name='reset_password'),
]
if settings.DEBUG:  # Solo para desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)