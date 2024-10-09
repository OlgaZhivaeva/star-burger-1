from pprint import pprint
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.templatetags.static import static
from django.shortcuts import get_object_or_404

from .models import Product, Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):

    data = request.data
    pprint(data)
    order = Order.objects.create(
        address=data['address'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        phonenumber=data['phonenumber']
    )
    try:
        if data['products'] == []:
            return Response({'error': 'Не указаны продукты для заказа (пустой список)'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['products'], list):
            return Response({'error': 'Неверно указаны продукты для заказа'}, status=status.HTTP_400_BAD_REQUEST)
        for ordered_product in data['products']:
            product = get_object_or_404(Product, id=ordered_product['product'])
            quantity = ordered_product['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
        return Response({'error': 'Заказ сохранен'}, status=status.HTTP_201_CREATED)
    except KeyError:
        return Response({'error': 'Не указаны продукты для заказа'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Response({'error': 'Ошибка при сохранении заказа'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

