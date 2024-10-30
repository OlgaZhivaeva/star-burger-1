from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class OrderQuerySet(models.QuerySet):
    def calculate_total_cost(self):
        orders = self.annotate(total_cost=Sum(F('products__price') * F('products__quantity')))
        return orders


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=300,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f'{self.restaurant.name} - {self.product.name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('UNPROCESSED', 'Необработанный'),
        ('ASSEMBLY', 'Сборка'),
        ('DELIVERY', 'Доставка'),
        ('COMPLETED', 'Выполнен'),
    ]
    PYMENT_CHOICES = [
        ('IN_CASH', 'Наличностью'),
        ('ELECTRONICLLY', 'Электронно')
    ]
    address = models.CharField(
        verbose_name='адрес доставки',
        max_length=200,
        blank=True
    )
    firstname = models.CharField(
        verbose_name='имя',
        max_length=200
    )
    lastname = models.CharField(
        verbose_name='фамилия',
        max_length=200,
        blank=True
    )
    phonenumber = PhoneNumberField(
        verbose_name='номер телефона',
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name='статус заказа',
        max_length=11,
        choices=STATUS_CHOICES,
        default='UNPROCESSED',
        db_index=True
    )
    comment = models.TextField(
        verbose_name='комментарий',
        blank=True
    )
    registered_at = models.DateTimeField(
        verbose_name='время регистрации',
        db_index=True,
        auto_now_add=True
    )
    called_at = models.DateTimeField(
        verbose_name='время звонка',
        blank=True,
        null=True,
        db_index=True
    )
    delivered_at = models.DateTimeField(
        verbose_name='время доставки',
        blank=True,
        null=True,
        db_index=True
    )
    payment_method = models.CharField(
        max_length=11,
        choices=PYMENT_CHOICES,
        blank=True,
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='готовит ресторан',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.address}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='products',
        blank=True,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        related_name='products',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)])
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=False
    )

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'
        unique_together = [
            ['order', 'product']
        ]

    def __str__(self):
        return f'{self.product.name} {self.quantity}'
