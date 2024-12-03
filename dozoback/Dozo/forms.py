from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # type: ignore
from .models import CustomUser, Producto, Categoria, Carrito, Venta

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'telefono',
            'department', 'city', 'address', 'postal_code', 'password1', 'password2', 'role'
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 
            'department', 'city', 'address', 'postal_code','role'
        )

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('imagen', 'titulo', 'descripcion', 'talla', 'precio', 'categoria', 'estado')

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre',)

class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ('usuario', 'producto', 'cantidad')

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ('usuario', 'estado')

