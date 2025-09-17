from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User, Group

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'штуки'),
        ('kg', 'килограммы'),
        ('l', 'литры'),
    ]
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    image = models.ImageField(upload_to='manufacturers/', blank=True, null=True)

    def __str__(self):
        return self.name

class PromoCode(models.Model):
    code = models.CharField(max_length=20)
    discount_percent = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Время входа")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Время выхода")
    session_key = models.CharField(max_length=40, db_index=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)

    def __str__(self):
        name = self.user.get_full_name()
        if not name:
            name = self.user.username
        return f"Клиент: {name} (ID: {self.id})"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Добавляем в группу client при сохранении
        client_group = Group.objects.get(name='client')
        self.user.groups.add(client_group)
        # Удаляем из группы employee (если был там)
        employee_group = Group.objects.get(name='employee')
        self.user.groups.remove(employee_group)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    department = models.CharField(max_length=100, verbose_name='Отдел')
    position = models.CharField(max_length=100, verbose_name='Должность', blank=True)
    bio = models.TextField(verbose_name='Описание работ', blank=True)
    photo = models.ImageField(
        upload_to='employees/',
        verbose_name='Фото сотрудника',
        blank=True,
        null=True
    )
    is_visible = models.BooleanField(default=True, verbose_name='Отображать на сайте')

    def __str__(self):
        name = self.user.get_full_name()
        if not name:
            name = self.user.username
        position = f", {self.position}" if self.position else ""
        return f"Сотрудник: {name}{position}"

    def photo_tag(self):
        if self.photo and hasattr(self.photo, 'url'):
            return mark_safe(f'<img src="{self.photo.url}" width="150" height="150" />')
        return "Нет фото"

    photo_tag.short_description = 'Фото'
    photo_tag.allow_tags = True

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Добавляем в группу employee при сохранении
        employee_group = Group.objects.get(name='employee')
        self.user.groups.add(employee_group)
        # Удаляем из группы client (если был там)
        client_group = Group.objects.get(name='client')
        self.user.groups.remove(client_group)

class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Корзина'),
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        verbose_name="Клиент"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа"
    )
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def total_cost(self):
        total = sum(item.total_price for item in self.items.all())
        if self.promo_code and self.promo_code.active:
            discount = total * self.promo_code.discount_percent / 100
            return total - discount
        return total

    def __str__(self):
        return f"Заказ #{self.id} от {self.client.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class AboutCompany(models.Model):
    """Основная информация о компании"""
    title = models.CharField(_('Заголовок'), max_length=200)
    short_description = models.TextField(_('Краткое описание'))
    full_description = models.TextField(_('Полное описание'))
    logo = models.ImageField(_('Логотип компании'), upload_to='about/logo/', blank=True, null=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    video_url = models.URLField(_('Видео'), blank=True, null=True)
    history = models.TextField(_('История'), blank=True, null=True)
    requisites = models.TextField(_('Реквизиты'), blank=True, null=True)
    certificate = models.TextField(_('Сертификат'), blank=True, null=True)

    def __str__(self):
        return self.title


class NewsArticle(models.Model):
    title = models.CharField(_('Заголовок'), max_length=200)
    short_description = models.CharField(_('Краткое описание'), max_length=200)
    full_content = models.TextField(_('Полное содержание'))
    image = models.ImageField(_('Изображение'), upload_to='news/')
    publication_date = models.DateTimeField(_('Дата публикации'), auto_now_add=True)
    is_published = models.BooleanField(_('Опубликовано'), default=True)
    category = models.CharField(_('Категория'), max_length=50, blank=True)
    youtube_url = models.URLField(
        _('Ссылка на YouTube видео'),
        blank=True,
        null=True,
        help_text="Вставьте ссылку на видео с YouTube"
    )


    def __str__(self):
        return self.title


class FAQItem(models.Model):
    question = models.CharField(_('Вопрос'), max_length=255)
    answer = models.TextField(_('Ответ'))
    date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)
    category = models.CharField(_('Категория'), max_length=50, blank=True)
    is_featured = models.BooleanField(_('Популярный вопрос'), default=False)


    def __str__(self):
        return self.question

class PrivacyPolicy(models.Model):
    content = models.TextField(_('Содержание'))
    last_updated = models.DateTimeField(_('Последнее обновление'), auto_now=True)

    def __str__(self):
        return f"Политика конфиденциальности ({self.last_updated.date()})"


class JobVacancy(models.Model):
    POSITION_CHOICES = [
        ('full', 'Полная занятость'),
        ('part', 'Частичная занятость'),
        ('remote', 'Удалённая работа'),
    ]

    title = models.CharField(_('Должность'), max_length=200)
    description = models.TextField(_('Описание'))
    requirements = models.TextField(_('Требования'))
    position_type = models.CharField(
        _('Тип занятости'),
        max_length=10,
        choices=POSITION_CHOICES,
        default='full'
    )
    salary = models.CharField(_('Зарплата'), max_length=100, blank=True)
    is_active = models.BooleanField(_('Активная вакансия'), default=True)
    published_date = models.DateTimeField(_('Дата публикации'), auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Пользователь')
    )
    author_name = models.CharField(_('Имя автора'), max_length=100)
    rating = models.PositiveSmallIntegerField(
        _('Оценка'),
        choices=RATING_CHOICES,
        default=5
    )
    text = models.TextField(_('Текст отзыва'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.author_name} ({self.created_at.date()})"

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField()  # если баннер ведёт на сайт или акцию

    def __str__(self):
        return self.title

class CompanyPartner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    website_url = models.URLField()

    def __str__(self):
        return self.name