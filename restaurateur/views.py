from operator import itemgetter
import requests
from geopy.distance import distance
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views


from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from geocoords.models import Geocoords
from star_burger.settings import API_KEY_GEOCODER


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = Restaurant.objects.order_by('name')
    products = Product.objects.prefetch_related('menu_items')

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    def fetch_coordinates(apikey, address):
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        })
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lon, lat

    menu_items = RestaurantMenuItem.objects.filter(availability=True,).prefetch_related('restaurant')
    orders = Order.objects.all().prefetch_related('products__product').calculate_total_cost()

    for order in orders:
        all_restaurants = []
        for order_product in order.products.all():
            restaurants = []
            for menu_item in menu_items.filter(product=order_product.product.id):
                restaurants.append(menu_item.restaurant.name)
            all_restaurants.append(restaurants)

        restaurants_for_cook = []
        if not all_restaurants:
            order.no_restaurant_or_distance = 'Не нашлось одного ресторана'
        elif not all_restaurants[1:]:
            restaurants_for_cook = all_restaurants[0]
        else:
            restaurants_for_cook = set(all_restaurants[0]).intersection(*all_restaurants[1:])

        distances_to_restaurants = []
        if restaurants_for_cook:

            for restaurant in restaurants_for_cook:
                try:
                    if Geocoords.objects.filter(address=order.address):
                        address_coords = (Geocoords.objects.get(address=order.address).lon,
                                          Geocoords.objects.get(address=order.address).lat)
                    else:
                        address_coords = fetch_coordinates(API_KEY_GEOCODER, order.address)
                        if not address_coords:
                            order.no_restaurant_or_distance = 'Ошибка определения координат'
                            break
                        Geocoords.objects.create(address=order.address,
                                                 lon=address_coords[0],
                                                 lat=address_coords[1])

                    restaurant_address = Restaurant.objects.get(name=restaurant).address
                    if Geocoords.objects.filter(address=restaurant_address):
                        restaurant_coords = (Geocoords.objects.get(address=restaurant_address).lon,
                                             Geocoords.objects.get(address=restaurant_address).lat)
                    else:
                        restaurant_coords = fetch_coordinates(API_KEY_GEOCODER, restaurant_address)
                        if not restaurant_coords:
                            order.no_restaurant_or_distance = 'Ошибка определения координат'
                            break
                        Geocoords.objects.create(address=restaurant_address,
                                                 lon=restaurant_coords[0],
                                                 lat=restaurant_coords[1])

                    distance_to_restaurant = round(distance(restaurant_coords, address_coords).km, 2)

                except request.RequestException:
                    order.no_restaurant_or_distance = 'Ошибка определения координат'
                    break
                distances_to_restaurants.append((restaurant, distance_to_restaurant))
            order.distances_to_restaurants = sorted(distances_to_restaurants, key=itemgetter(1))

    return render(request, template_name='order_items.html', context={'order_items': orders})
