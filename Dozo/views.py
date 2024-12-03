from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth import login, authenticate, logout as auth_logout # type: ignore
from django.contrib.auth.forms import AuthenticationForm # type: ignore
from django.db import IntegrityError # type: ignore
from .models import CustomUser, Producto, Categoria, Carrito, Venta, VentaProducto, Producto, Estado
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProductoForm, CategoriaForm, CarritoForm, VentaForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

# User Views
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    user = form.save()
                    login(request, user)

                    # Enviar correo de bienvenida
                    try:
                        send_mail(
                            'Bienvenido a Dozo',
                            f'Hola {user.first_name}, gracias por registrarte en Dozo. ¡Esperamos que disfrutes de tu experiencia!',
                            'panzzz956@gmail.com',  # Remitente
                            [user.email],  # Receptor
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(f"Error al enviar correo de bienvenida: {str(e)}")

                    return redirect('mostrar_user')
                except IntegrityError:
                    return render(request, 'registrouser.html', {
                        'form': form,
                        'error': "Error al crear el usuario. Por favor, inténtalo de nuevo."
                    })
            else:
                return render(request, 'registrouser.html', {
                    'form': form,
                    'error': "Las contraseñas no coinciden."
                })
        else:
            return render(request, 'registrouser.html', {
                'form': form,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = CustomUserCreationForm()
        return render(request, 'registrouser.html', {'form': form})



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

# Mostrar usuarios con paginación
@login_required
def mostrar_user(request):
    users_list = CustomUser.objects.all()
    page = request.GET.get('page', 1)  # Obtener el número de página de los parámetros GET
    paginator = Paginator(users_list, 10)  # Mostrar 10 usuarios por página

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)  # Si la página no es un número, mostrar la primera página
    except EmptyPage:
        users = paginator.page(paginator.num_pages)  # Si está fuera de rango, mostrar la última página

    return render(request, 'mostrar_user.html', {
        'users': users
    })

# Editar un usuario
@login_required
def editar_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mostrar_user')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'editar_user.html', {
        'form': form,
        'user': user
    })

# Eliminar un usuario
@login_required
def eliminar_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('mostrar_user')
    return render(request, 'eliminar_user.html', {
        'user': user
    })



from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse
import json

@csrf_exempt
def loginzzz(request):
    if request.method == "POST":
        try:
            # Parsear los datos de la solicitud
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            User = get_user_model()
            try:
                # Buscar usuario por email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'El usuario no existe'}, status=400)

            # Verificar contraseña
            if not user.check_password(password):
                return JsonResponse({'error': 'Contraseña incorrecta'}, status=400)

            # Iniciar sesión
            login(request, user)

            # Enviar correo de inicio de sesión exitoso
            try:
                send_mail(
                    'Inicio de sesión exitoso',
                    f'Hola {user.first_name}, has iniciado sesión en Dozo con éxito.',
                    'panzzz956@gmail.com',  # Remitente
                    [user.email],        # Receptor
                    fail_silently=False,
                )
            except Exception as e:
                return JsonResponse({'error': f'Error al enviar el correo: {str(e)}'}, status=500)

            # Responder con detalles del usuario
            return JsonResponse({
                'message': 'Inicio de sesión exitoso',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    # Incluye otros campos si es necesario, como nombre completo, roles, etc.
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
import json

@csrf_exempt
@login_required
def logout_all_sessions(request):
    if request.method == "POST":
        try:
            user = request.user
            if user.is_authenticated:
                # Cerrar todas las sesiones activas del usuario
                user_sessions = Session.objects.filter(session_key__in=[
                    session.session_key for session in Session.objects.all()
                    if str(session.get_decoded().get('_auth_user_id')) == str(user.id)
                ])
                user_sessions.delete()

                # Cierra la sesión actual
                logout(request)

                return JsonResponse({"message": "Sesiones cerradas exitosamente."}, status=200)
            return JsonResponse({"error": "Usuario no autenticado."}, status=401)
        except Exception as e:
            return JsonResponse({"error": f"Error al cerrar sesiones: {str(e)}"}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

# Mostrar productos con paginación
@login_required
def mostrar_producto(request):
    productos_list = Producto.objects.all()
    page = request.GET.get('page', 1)  # Obtener el número de página de los parámetros GET
    paginator = Paginator(productos_list, 10)  # Mostrar 10 productos por página

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)  # Si la página no es un número, mostrar la primera página
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)  # Si está fuera de rango, mostrar la última página

    return render(request, 'productos/producto_list.html', {
        'productos': productos
    })

# Crear un producto
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('mostrar_producto')
            except Exception as e:
                return render(request, 'productos/producto_create.html', {
                    'form': form,
                    'error': f"Error al crear el producto: {str(e)}"
                })
        else:
            return render(request, 'productos/producto_create.html', {
                'form': form,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = ProductoForm()
        return render(request, 'productos/producto_create.html', {
            'form': form
        })

# Editar un producto
@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            try:
                form.save()
                return redirect('mostrar_producto')
            except Exception as e:
                return render(request, 'productos/producto_edit.html', {
                    'form': form,
                    'producto': producto,
                    'error': f"Error al actualizar el producto: {str(e)}"
                })
        else:
            return render(request, 'productos/producto_edit.html', {
                'form': form,
                'producto': producto,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = ProductoForm(instance=producto)
        return render(request, 'productos/producto_edit.html', {
            'form': form,
            'producto': producto
        })

# Eliminar un producto
@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        try:
            producto.delete()
            return redirect('mostrar_producto')
        except Exception as e:
            return render(request, 'productos/producto_delete.html', {
                'producto': producto,
                'error': f"Error al eliminar el producto: {str(e)}"
            })
    return render(request, 'productos/producto_delete.html', {
        'producto': producto
    })



# Categoria Views
# Mostrar categorías
@login_required
def mostrar_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categoria_list.html', {'categorias': categorias})


# Crear una nueva categoría
@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('mostrar_categoria')
            except Exception as e:
                return render(request, 'categorias/categoria_create.html', {
                    'form': form,
                    'error': f"Error al crear la categoría: {str(e)}"
                })
        else:
            return render(request, 'categorias/categoria_create.html', {
                'form': form,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = CategoriaForm()
        return render(request, 'categorias/categoria_create.html', {
            'form': form
        })

# Editar una categoría
@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            try:
                form.save()
                return redirect('mostrar_categoria')
            except Exception as e:
                return render(request, 'categorias/categoria_edit.html', {
                    'form': form,
                    'categoria': categoria,
                    'error': f"Error al actualizar la categoría: {str(e)}"
                })
        else:
            return render(request, 'categorias/categoria_edit.html', {
                'form': form,
                'categoria': categoria,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = CategoriaForm(instance=categoria)
        return render(request, 'categorias/categoria_edit.html', {
            'form': form,
            'categoria': categoria
        })

# Eliminar una categoría
@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        try:
            categoria.delete()
            return redirect('mostrar_categoria')
        except Exception as e:
            return render(request, 'categorias/categoria_delete.html', {
                'categoria': categoria,
                'error': f"Error al eliminar la categoría: {str(e)}"
            })
    return render(request, 'categorias/categoria_delete.html', {
        'categoria': categoria
    })

# Carrito Viewsfrom

# Crear un carrito
@login_required
def crear_carrito(request):
    if request.method == 'POST':
        form = CarritoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('mostrar_carrito')
            except Exception as e:
                return render(request, 'carritos/carrito_create.html', {
                    'form': form,
                    'error': f"Error al crear el carrito: {str(e)}"
                })
        else:
            return render(request, 'carritos/carrito_create.html', {
                'form': form,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = CarritoForm()
        return render(request, 'carritos/carrito_create.html', {
            'form': form
        })



# Venta Viewsfrom

# Mostrar ventas
@login_required
def mostrar_venta(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/venta_list.html', {
        'ventas': ventas
    })

# Crear una venta
@csrf_exempt
def crear_venta_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not data.get('user') or not data.get('cart'):
                return JsonResponse({'error': 'El payload debe contener "user" y "cart".'}, status=400)

            user_data = data['user']
            cart = data['cart']

            try:
                usuario = CustomUser.objects.get(email=user_data.get('email'))
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)

            estado, created = Estado.objects.get_or_create(nombre="Pendiente")
            total = sum(float(item['precio']) * item['cantidad'] for item in cart)
            venta = Venta.objects.create(usuario=usuario, total=total, estado=estado)

            for item in cart:
                try:
                    producto = Producto.objects.get(id=item['id'])
                    VentaProducto.objects.create(
                        venta=venta,
                        producto=producto,
                        precio_unidad=float(producto.precio),
                        cantidad=item['cantidad']
                    )
                except Producto.DoesNotExist:
                    return JsonResponse({'error': f'Producto con ID {item["id"]} no encontrado.'}, status=404)

            # Enviar correo de confirmación de pedido
            try:
                productos_detalle = "\n".join(
                    f"- {item['cantidad']}x {item['titulo']} (${item['precio']} c/u)" for item in cart
                )
                send_mail(
                    'Confirmación de Pedido - Dozo',
                    f'Hola {usuario.first_name}, tu pedido ha sido confirmado.\n\n'
                    f'Detalles del pedido:\n{productos_detalle}\n\n'
                    f'Total: ${total}\n\nGracias por tu compra en Dozo.',
                    'panzzz956@gmail.com',
                    [usuario.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar correo de confirmación de pedido: {str(e)}")

            return JsonResponse({'message': 'Venta creada exitosamente.', 'venta_id': venta.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al parsear JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


# Editar una venta
@login_required
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            try:
                form.save()
                return redirect('mostrar_venta')
            except Exception as e:
                return render(request, 'ventas/venta_edit.html', {
                    'form': form,
                    'venta': venta,
                    'error': f"Error al actualizar la venta: {str(e)}"
                })
        else:
            return render(request, 'ventas/venta_edit.html', {
                'form': form,
                'venta': venta,
                'error': "Hay errores en la información ingresada. Por favor, revisa los campos."
            })
    else:
        form = VentaForm(instance=venta)
        return render(request, 'ventas/venta_edit.html', {
            'form': form,
            'venta': venta
        })

# Eliminar una venta
@login_required
def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        try:
            venta.delete()
            return redirect('mostrar_venta')
        except Exception as e:
            return render(request, 'ventas/venta_delete.html', {
                'venta': venta,
                'error': f"Error al eliminar la venta: {str(e)}"
            })
    return render(request, 'ventas/venta_delete.html', {
        'venta': venta
    })



from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoSerializer
@login_required
class ProductoListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.filter(estado=True)  # Solo productos activos
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)



from rest_framework.generics import RetrieveAPIView
from .models import Producto
from .serializers import ProductoSerializer
@login_required
class ProductoDetailAPIView(RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer



# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, Producto
from .serializers import CartSerializer, CartItemSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Producto.objects.get(id=request.data['product_id'])
        item, item_created = cart.items.get_or_create(product=product)
        if not item_created:
            item.quantity += request.data.get('quantity', 1)
        else:
            item.quantity = request.data.get('quantity', 1)
        item.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def delete(self, request, item_id):
        cart = Cart.objects.get(user=request.user)
        item = cart.items.get(id=item_id)
        item.delete()
        serializer = CartSerializer(cart)
        return Response(serializer.data)


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Venta, VentaProducto

@login_required
def listar_pedidos_usuario(request):
    try:
        usuario = request.user
        ventas = Venta.objects.filter(usuario=usuario).select_related('estado')

        pedidos = [
            {
                "id": venta.id,
                "fecha_venta": venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S'),
                "estado": venta.estado.nombre,
                "total": float(venta.total),
                "productos": [
                    {
                        "titulo": vp.producto.titulo,
                        "cantidad": vp.cantidad,
                        "precio": float(vp.precio_unidad),
                    }
                    for vp in VentaProducto.objects.filter(venta=venta)
                ]
            }
            for venta in ventas
        ]

        return JsonResponse({"pedidos": pedidos}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Error al obtener pedidos: {str(e)}"}, status=500)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer

class RegisterUserView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)

        print("Errores del serializer:", serializer.errors)  # Imprime errores en consola
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



from django.http import JsonResponse
from .models import Producto

def filter_products(request):
    # Obtener los filtros desde los parámetros GET
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_id = request.GET.get('category_id')

    # Depuración: Imprimir los filtros recibidos
    print(f"Min price: {min_price}, Max price: {max_price}, Category id: {category_id}")

    # Convierte los precios a enteros si se proporcionan
    try:
        if min_price:
            min_price = int(min_price)
        if max_price:
            max_price = int(max_price)
    except ValueError:
        return JsonResponse({"error": "Invalid price values"}, status=400)

    # Filtra los productos
    products = Producto.objects.all()

    if min_price is not None:
        print(f"Filtrando por precio mínimo: {min_price}")
        products = products.filter(precio__gte=min_price)
    if max_price is not None:
        print(f"Filtrando por precio máximo: {max_price}")
        products = products.filter(precio__lte=max_price)
    if category_id:
        print(f"Filtrando por categoría: {category_id}")
        products = products.filter(categoria_id=category_id)

    # Serializa los productos
    products_data = [
        {
            "id": p.id,
            "titulo": p.titulo,
            "precio": p.precio,
            "categoria": {"id": p.categoria.id, "nombre": p.categoria.nombre} if p.categoria else None,
            "descripcion": p.descripcion,
            "imagen": p.imagen.url if p.imagen else None,  # Asegúrate de que `imagen` esté disponible
        }
        for p in products
    ]

    # Depuración: Verificar los productos filtrados
    print(f"Productos filtrados: {products_data}")

    return JsonResponse(products_data, safe=False)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Venta
from .serializers import VentaSerializer
@login_required
class PedidoDetailView(APIView):
    def get(self, request, id):
        try:
            venta = Venta.objects.get(id=id)
            serializer = VentaSerializer(venta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Venta.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@login_required
class VentaAPIView(APIView):
    def post(self, request):
        try:
            # Procesa la solicitud
            data = request.data
            venta = Venta.objects.create(**data)
            return Response({"message": "Venta creada correctamente"}, status=201)
        except Exception as e:
            # Log para depurar
            print(f"Error: {e}")
            return Response({"error": "Error interno del servidor"}, status=500)


from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum, F, Min, Max
from .models import Venta, VentaProducto, Producto
from django.db.models.functions import TruncMonth, TruncDay
@login_required
def ventas_view(request):
    # Recuperar todas las ventas con sus productos
    ventas = Venta.objects.select_related('usuario', 'estado').prefetch_related('productos')

    # Paginación
    paginator = Paginator(ventas, 10)  # Mostrar 10 ventas por página
    page_number = request.GET.get('page')
    ventas_paginadas = paginator.get_page(page_number)

    # Obtener datos para el gráfico de productos más vendidos
    productos_mas_vendidos = (
        VentaProducto.objects
        .values('producto__titulo')
        .annotate(total_vendido=Sum(F('cantidad')))
        .order_by('-total_vendido')[:10]
    )

    # Producto más vendido
    producto_mas_vendido = (
        VentaProducto.objects
        .values('producto__titulo')
        .annotate(total_vendido=Sum(F('cantidad')))
        .order_by('-total_vendido')
        .first()
    )

    # Producto menos vendido
    producto_menos_vendido = (
        VentaProducto.objects
        .values('producto__titulo')
        .annotate(total_vendido=Sum(F('cantidad')))
        .order_by('total_vendido')
        .first()
    )

    # Producto más costoso
    producto_mas_costoso = Producto.objects.order_by('-precio').first()

    # Producto más barato
    producto_mas_barato = Producto.objects.order_by('precio').first()

    # Calcular el subtotal de todas las ventas
    subtotal = ventas.aggregate(total=Sum('total'))['total'] or 0

    # Calcular las ganancias por fecha
    ganancias = (
        Venta.objects
        .values('fecha_venta__date')
        .annotate(total_ganancias=Sum('total'))
        .order_by('fecha_venta__date')
    )

    # Ventas diarias
    ventas_diarias = (
        Venta.objects
        .annotate(dia=TruncDay('fecha_venta'))
        .values('dia')
        .annotate(total_ventas=Sum('total'))
        .order_by('dia')
    )

    # Ventas mensuales
    ventas_mensuales = (
        Venta.objects
        .annotate(mes=TruncMonth('fecha_venta'))
        .values('mes')
        .annotate(total_ventas=Sum('total'))
        .order_by('mes')
    )

    # Contexto para pasar a la plantilla
    context = {
        'ventas': ventas_paginadas,  # Paginación aplicada aquí
        'productos_mas_vendidos': productos_mas_vendidos,
        'producto_mas_vendido': producto_mas_vendido,
        'producto_menos_vendido': producto_menos_vendido,
        'producto_mas_costoso': producto_mas_costoso,
        'producto_mas_barato': producto_mas_barato,
        'subtotal': subtotal,
        'ganancias': ganancias,
        'ventas_diarias': ventas_diarias,
        'ventas_mensuales': ventas_mensuales,
    }
    return render(request, 'ventas.html', context)


from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer

@api_view(['GET'])
@login_required
def user_profile(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)




from django.http import JsonResponse
from .models import VentaProducto

def productos_mas_vendidos(request):
    try:
        # Obtener los productos vendidos (sin total vendido)
        productos_vendidos = (
            VentaProducto.objects
            .values(
                'producto__id',
                'producto__titulo',
                'producto__precio',
                'producto__imagen',
                'producto__descripcion'
            )
            .distinct()  # Elimina duplicados si se da el caso
        )

        # Serializar los datos
        productos_data = [
            {
                "id": producto['producto__id'],
                "titulo": producto['producto__titulo'],
                "precio": float(producto['producto__precio']),  # Convertir Decimal a float
                "imagen": producto['producto__imagen'] if producto['producto__imagen'] else "default.png",
                "descripcion": producto['producto__descripcion'],
            }
            for producto in productos_vendidos
        ]

        # Asegurarnos de que las URLs de las imágenes sean accesibles
        for producto in productos_data:
            if producto['imagen'] != "default.png":
                producto['imagen'] = f"/media/{producto['imagen']}"  # Ruta completa para las imágenes

        return JsonResponse({"productos": productos_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Error al obtener los productos más vendidos: {str(e)}"}, status=500)



from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@login_required
@csrf_exempt
def edit_user_profile(request):
    if request.method == 'PUT':
        try:
            user = request.user  # Obtén el usuario autenticado
            data = json.loads(request.body)  # Obtén los datos de la solicitud
            changes = []  # Lista para almacenar los cambios realizados

            # Verifica y actualiza cada campo
            if data.get('email') and data.get('email') != user.email:
                changes.append(f"Correo: {user.email} → {data['email']}")
                user.email = data['email']

            if data.get('first_name') and data.get('first_name') != user.first_name:
                changes.append(f"Nombre: {user.first_name} → {data['first_name']}")
                user.first_name = data['first_name']

            if data.get('last_name') and data.get('last_name') != user.last_name:
                changes.append(f"Apellido: {user.last_name} → {data['last_name']}")
                user.last_name = data['last_name']

            if data.get('telefono') and data.get('telefono') != user.telefono:
                changes.append(f"Teléfono: {user.telefono} → {data['telefono']}")
                user.telefono = data['telefono']

            if data.get('department') and data.get('department') != user.department:
                changes.append(f"Departamento: {user.department} → {data['department']}")
                user.department = data['department']

            if data.get('city') and data.get('city') != user.city:
                changes.append(f"Ciudad: {user.city} → {data['city']}")
                user.city = data['city']

            if data.get('postal_code') and data.get('postal_code') != user.postal_code:
                changes.append(f"Código postal: {user.postal_code} → {data['postal_code']}")
                user.postal_code = data['postal_code']

            if data.get('address') and data.get('address') != user.address:
                changes.append(f"Dirección: {user.address} → {data['address']}")
                user.address = data['address']

            user.save()  # Guarda los cambios en la base de datos

            # Enviar correo al usuario
            if changes:
                message = (
                    f"Hola {user.first_name},\n\n"
                    "Tu información en Dozo ha sido actualizada con éxito. Estos son los cambios realizados:\n\n"
                    + "\n".join(changes) +
                    "\n\nSi no reconoces estos cambios, contacta con nuestro equipo de soporte inmediatamente.\n\n"
                    "Gracias por usar nuestros servicios.\n\n"
                    "El equipo de Dozo"
                )
                send_mail(
                    subject="Información actualizada en Dozo",
                    message=message,
                    from_email=None,  # Usará DEFAULT_FROM_EMAIL
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            return JsonResponse({'message': 'Perfil actualizado exitosamente.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error al actualizar el perfil: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)



from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required
def verify_current_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            current_password = data.get("current_password")
            user = request.user

            if not check_password(current_password, user.password):
                return JsonResponse({"error": "Contraseña incorrecta"}, status=400)

            return JsonResponse({"message": "Contraseña verificada correctamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)



from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required
def change_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_password = data.get("new_password")
            user = request.user

            user.set_password(new_password)
            user.save()

            # Enviar notificación por correo
            send_mail(
                "Cambio de Contraseña en Dozo",
                f"Hola {user.first_name}, tu contraseña ha sido cambiada exitosamente.",
                "noreply@dozo.com",
                [user.email],
                fail_silently=False,
            )

            return JsonResponse({"message": "Contraseña cambiada correctamente"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Venta, VentaProducto

@login_required
def listar_pedidos_usuario(request):
    try:
        usuario = request.user
        ventas = Venta.objects.filter(usuario=usuario).select_related('estado')

        pedidos = [
            {
                "id": venta.id,
                "fecha_venta": venta.fecha_venta.strftime('%Y-%m-%d %H:%M:%S'),
                "estado": venta.estado.nombre,
                "total": float(venta.total),
                "productos": [
                    {
                        "titulo": vp.producto.titulo,
                        "cantidad": vp.cantidad,
                        "precio": float(vp.precio_unidad),
                    }
                    for vp in VentaProducto.objects.filter(venta=venta)
                ]
            }
            for venta in ventas
        ]

        return JsonResponse({"pedidos": pedidos}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Error al obtener pedidos: {str(e)}"}, status=500)




from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import json

User = get_user_model()

@csrf_exempt
def send_reset_password_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = User.objects.get(email=email)
            reset_url = f"https://dozo01.pythonanywhere.com/reset-password/{user.id}"  # URL para el frontend
            send_mail(
                subject="Restablecer contraseña",
                message=f"Utiliza el siguiente enlace para restablecer tu contraseña: {reset_url}",
                from_email="noreply@dozo.com",
                recipient_list=[email],
            )
            return JsonResponse({"message": "Correo enviado con éxito.", "user_id": user.id}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "Correo no encontrado."}, status=404)
    return JsonResponse({"error": "Método no permitido."}, status=405)


@csrf_exempt
def reset_password(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_password = data.get("new_password")

            if not new_password:
                return JsonResponse({"error": "La nueva contraseña es obligatoria."}, status=400)

            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()

            return JsonResponse({"message": "Contraseña actualizada exitosamente."}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido."}, status=405)

