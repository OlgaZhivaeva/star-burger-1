import re
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


    try:
        if data['address'] == None:
            return Response({'error': 'Поле адрес не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['address'], str):
            return Response({'error': 'Поле адрес должно быть строкой'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'Поле адрес обязательно к заполнению'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if data['firstname'] == None:
            return Response({'error': 'Поле имя не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['firstname'], str):
            return Response({'error': 'Поле имя должно быть строкой'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'Поле имя обязательно к заполнению'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if data['lastname'] == None:
            return Response({'error': 'Поле фамилия не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['lastname'], str):
            return Response({'error': 'Поле фамилия должно быть строкой'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'Поле фамилия обязательно к заполнению'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if data['phonenumber'] == '':
            return Response({'error': 'Поле phonenumber не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['phonenumber'], str):
            return Response({'error': 'Поле телефон должно быть строкой'}, status=status.HTTP_400_BAD_REQUEST)
        phone_pattern = r'^(\+7)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
        if not re.match(phone_pattern, data['phonenumber']):
            return Response({'error': 'Не корректный номер телефона'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'Поле телефон обязательно к заполнению'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if data['products'] == []:
            return Response({'error': 'Не указаны продукты для заказа (пустой список)'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(data['products'], list):
            return Response({'error': 'Неверно указаны продукты для заказа'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'Не указаны продукты для заказа'}, status=status.HTTP_400_BAD_REQUEST)

    for ordered_product in data['products']:
        try:
            if not isinstance(ordered_product['product'], int):
                return Response({'error': 'id продукта должен быть целым числом'},status=status.HTTP_400_BAD_REQUEST)
            try:
                Product.objects.get(id=ordered_product['product'])
            except Product.DoesNotExist:
                return Response({'error': 'Указан не существующий id продукта'},status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Не указаны продукты для заказа'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if not isinstance(ordered_product['quantity'], int):
                return Response({'error': 'Количество должно быть целым числом'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Не указано количество продуктов для заказа'}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        address=data['address'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        phonenumber=data['phonenumber']
    )
    for ordered_product in data['products']:
        product = get_object_or_404(Product, id=ordered_product['product'])
        quantity = ordered_product['quantity']
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
    return Response({'error': 'Заказ сохранен'}, status=status.HTTP_201_CREATED)
