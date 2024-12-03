from rest_framework import serializers
from .models import Producto, Categoria, Cart, CartItem, CustomUser

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'  # Incluye todos los campos del modelo Categoria

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
        
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 
            'first_name', 'last_name', 
            'department', 'city', 'address', 
            'postal_code', 'role', 'telefono'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Oculta la contraseña en las respuestas
            'email': {'required': True},      # Marca el email como obligatorio
        }

    def create(self, validated_data):
        # Crear el usuario con un método que maneje contraseñas
        return CustomUser.objects.create_user(**validated_data)
    
    from rest_framework import serializers
from .models import Venta, VentaProducto, Producto

# Serializer de Producto
from rest_framework import serializers
from .models import Producto, Categoria

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'titulo', 'precio', 'descripcion', 'categoria', 'imagen']

    def get_categoria(self, obj):
        return {"id": obj.categoria.id, "nombre": obj.categoria.nombre} if obj.categoria else None





class VentaProductoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = VentaProducto
        fields = ['producto', 'precio_unidad', 'cantidad']

class VentaSerializer(serializers.ModelSerializer):
    productos = VentaProductoSerializer(many=True, read_only=True)
    estado = serializers.StringRelatedField()

    class Meta:
        model = Venta
        fields = ['id', 'usuario', 'fecha_venta', 'total', 'estado', 'productos']
