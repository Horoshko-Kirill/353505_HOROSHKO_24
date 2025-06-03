from django.http import Http404
import calendar
import requests
from .forms import ClientRegistrationForm, EmployeeRegistrationForm
from .models import Client, Employee
from django.contrib.auth import logout as auth_logout
from .forms import ManufacturerForm
from django.db.models import Q
from .models import Product, ProductCategory, Manufacturer
from .forms import ProductForm
from .models import PromoCode
from .models import AboutCompany
from .models import NewsArticle
from .models import FAQItem
from .models import JobVacancy
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Review
from .forms import ReviewForm
from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Product, Order, OrderItem, Client
import matplotlib.pyplot as plt
import io
import base64
from django.utils.timezone import now
from django.contrib.auth.models import User



def home(request):
    utc_time = timezone.now()
    local_time = timezone.localtime(utc_time)
    cal = calendar.TextCalendar()
    current_month_calendar = cal.formatmonth(local_time.year, local_time.month)

    try:
        response = requests.get('https://official-joke-api.appspot.com/random_ten')
        response.raise_for_status()
        jokes = response.json()[:3]
    except Exception:
        jokes = [
            {"setup": "Не удалось загрузить шутки", "punchline": "Попробуйте обновить страницу."}
        ]

    return render(request, 'shop/home.html', {
        'utc_time': utc_time,
        'local_time': local_time,
        'calendar': current_month_calendar,
        'jokes': jokes,
    })

def about(request):
    # Получаем первую запись о компании (или None, если нет данных)
    company_info = AboutCompany.objects.first()
    return render(request, 'shop/about.html', {
        'company': company_info
    })


def careers(request):
    # Получаем только активные вакансии, отсортированные по дате публикации (новые сначала)
    vacancies = JobVacancy.objects.filter(is_active=True).order_by('-published_date')

    # Группируем вакансии по типу занятости
    position_types = {
        'full': 'Полная занятость',
        'part': 'Частичная занятость',
        'remote': 'Удалённая работа'
    }

    context = {
        'vacancies': vacancies,
        'position_types': position_types,
    }

    return render(request, 'shop/careers.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='client').exists())
def client_orders(request):
    client = get_object_or_404(Client, user=request.user)
    orders = Order.objects.filter(client=client).exclude(status='cart').order_by('-order_date')
    return render(request, 'shop/client_orders.html', {'orders': orders})

def contacts(request):
    # Получаем только видимых сотрудников, отсортированных по отделу
    employees = Employee.objects.filter(is_visible=True).order_by('department', 'position')

    # Группируем сотрудников по отделам
    departments = {}
    for employee in employees:
        if employee.department not in departments:
            departments[employee.department] = []
        departments[employee.department].append(employee)

    context = {
        'departments': departments,
    }

    return render(request, 'shop/contacts.html', context)

def coupons(request):
    active_promocodes = PromoCode.objects.filter(active=True).order_by('code')
    return render(request, 'shop/coupons.html', {
        'promocodes': active_promocodes
    })

@login_required
def employee_orders(request):
    # Предполагаем, что сотрудник — это пользователь, связанный с моделью Employee.
    try:
        employee = request.user.employee  # если связь один к одному User -> Employee
    except AttributeError:
        # Если у пользователя нет сотрудника — показать ошибку или пустой список
        orders = []
    else:
        # Берём заказы, где employee = текущий сотрудник
        orders = Order.objects.filter(employee=employee).order_by('-order_date')

    return render(request, 'shop/employee_orders.html', {'orders': orders})

def faq(request):
    # Получаем все вопросы, отсортированные по дате (новые сначала)
    faq_items = FAQItem.objects.all().order_by('-date_added')

    # Если нужно разделить по категориям
    categories = set(item.category for item in faq_items if item.category)

    # Если нужно выделить популярные вопросы
    featured_questions = FAQItem.objects.filter(is_featured=True)

    context = {
        'faq_items': faq_items,
        'categories': categories,
        'featured_questions': featured_questions,
    }

    return render(request, 'shop/faq.html', context)

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Пожалуйста, заполните все поля')
            return render(request, 'shop/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:  # Если пользователь аутентифицирован
            auth_login(request, user)  # Это критически важная строка - выполняет вход
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'shop/login.html')

    return render(request, 'shop/login.html')
def logout(request):
    auth_logout(request)
    return redirect('auth_options')

def auth_options(request):
    return render(request, 'shop/auth_options.html')

def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Создаем клиента
            Client.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                date_of_birth=form.cleaned_data['date_of_birth']
            )

            auth_login(request, user)
            return redirect('home')
    else:
        form = ClientRegistrationForm()
    return render(request, 'shop/register_client.html', {'form': form})


def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Создаем сотрудника
            Employee.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                department=form.cleaned_data['department'],
                position=form.cleaned_data['position'],
                bio=form.cleaned_data['bio'],
                photo=form.cleaned_data['photo'],
                is_visible=form.cleaned_data['is_visible']
            )

            auth_login(request, user)
            return redirect('home')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'shop/register_employee.html', {'form': form})

def auth_options(request):
    return render(request, 'shop/auth_options.html')


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def manufacturers(request):
    manufacturers_list = Manufacturer.objects.all().order_by('name')
    return render(request, 'shop/manufacturers.html', {
        'manufacturers': manufacturers_list
    })


@login_required
@user_passes_test(is_admin)
def add_manufacturer(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Производитель успешно добавлен')
            return redirect('manufacturers')
    else:
        form = ManufacturerForm()

    return render(request, 'shop/manufacturer_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def add_manufacturer(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Производитель добавлен')
            return redirect('manufacturers')
    else:
        form = ManufacturerForm()

    return render(request, 'shop/add_manufacturer.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_manufacturer(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES, instance=manufacturer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены')
            return redirect('manufacturers')
    else:
        form = ManufacturerForm(instance=manufacturer)

    return render(request, 'shop/manufacturer_form.html', {
        'form': form,
        'title': 'Редактировать производителя',
        'manufacturer': manufacturer
    })


@login_required
@user_passes_test(is_admin)
def delete_manufacturer(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        manufacturer.delete()
        messages.success(request, 'Производитель удален')
        return redirect('manufacturers')

    return render(request, 'shop/confirm_delete.html', {
        'object': manufacturer,
        'title': 'Удалить производителя'
    })


def news(request):
    articles = NewsArticle.objects.filter(is_published=True).order_by('-publication_date')

    # Добавляем embed_url для каждой статьи
    for article in articles:
        if article.youtube_url:
            article.embed_url = article.youtube_url.replace('watch?v=', 'embed/')

    context = {'articles': articles}
    return render(request, 'shop/news.html', context)

def privacy(request):
    return render(request, 'shop/privacy.html')

@login_required
@user_passes_test(is_admin)
def product_charts(request):
    users = User.objects.all()

    usernames = []
    total_times = []

    for user in users:
        visits = user.uservisit_set.all()
        total_duration = 0
        for visit in visits:
            if visit.logout_time:
                duration = visit.logout_time - visit.login_time
            else:
                duration = now() - visit.login_time
            total_duration += duration.total_seconds()

        usernames.append(user.username)
        total_times.append(total_duration / 3600)  # в часах

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.bar(usernames, total_times, color='skyblue')
    plt.xlabel('Пользователь')
    plt.ylabel('Время на сайте (часов)')
    plt.title('Общее время, проведённое пользователями на сайте')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Сохраняем график в буфер памяти
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    # Кодируем картинку в base64
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png).decode('utf-8')
    buffer.close()

    context = {
        'graphic': graphic,
    }

    return render(request, 'shop/product_charts.html', context)

def products(request):
    products_list = Product.objects.all()

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(manufacturer__name__icontains=search_query)
        )

    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        products_list = products_list.order_by('price')
    elif sort_by == 'price_desc':
        products_list = products_list.order_by('-price')
    elif sort_by == 'name':
        products_list = products_list.order_by('name')
    elif sort_by == 'newest':
        products_list = products_list.order_by('-id')

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products_list = products_list.filter(category_id=category_id)

    # Фильтрация по производителю
    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        products_list = products_list.filter(manufacturer_id=manufacturer_id)

    context = {
        'products': products_list,
        'categories': ProductCategory.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
        'search_query': search_query,
        'current_sort': sort_by,
        'selected_category': int(category_id) if category_id else None,
        'selected_manufacturer': int(manufacturer_id) if manufacturer_id else None,
    }
    return render(request, 'shop/products.html', context)


# CRUD операции (только для админа)
@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно добавлен')
            return redirect('products')
    else:
        form = ProductForm()

    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Добавить продукт'})


@login_required
@user_passes_test(is_admin)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт успешно обновлен')
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/product_form.html', {
        'form': form,
        'title': 'Редактировать продукт',
        'product': product
    })


@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Продукт удален')
        return redirect('products')

    return render(request, 'shop/confirm_delete.html', {
        'object': product,
        'title': 'Удалить продукт'
    })


def is_client(user):
    return user.groups.filter(name='client').exists()


def reviews(request):
    # Показываем все отзывы сразу (без модерации)
    reviews_list = Review.objects.all().order_by('-created_at')
    return render(request, 'shop/reviews.html', {'reviews': reviews_list})


@login_required
@user_passes_test(is_client, login_url='/accounts/login/')
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.author_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('reviews')
    else:
        form = ReviewForm()

    return render(request, 'shop/add_review.html', {'form': form})



@login_required
@user_passes_test(is_client, login_url='/accounts/login/')
def add_to_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    client = get_object_or_404(Client, user=request.user)

    if request.method == 'POST':
        try:
            quantity = Decimal(request.POST.get('quantity', '1'))
            if quantity <= Decimal('0'):
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, "Неверное количество товара")
            return redirect('products')

        # Ищем текущий активный заказ-корзину
        current_order = Order.objects.filter(
            client=client,
            status='cart'
        ).first()

        if not current_order:
            # Создаем новую корзину (заказ в статусе cart)
            current_order = Order.objects.create(
                client=client,
                delivery_date=timezone.now().date() + timedelta(days=3),
                status='cart'
            )

        # Добавляем товар в заказ
        order_item, created = OrderItem.objects.get_or_create(
            order=current_order,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        messages.success(request, f"Товар {product.name} добавлен в заказ")

    return redirect('products')


@login_required
@user_passes_test(is_client, login_url='/accounts/login/')
def current_order(request):
    try:
        client = Client.objects.get(user=request.user)
        current_order = Order.objects.filter(client=client, status='cart').first()  # Активная корзина
        employees = Employee.objects.all()
    except Client.DoesNotExist:
        current_order = None
        employees = []

    today = timezone.now().date()

    return render(request, 'shop/current_order.html', {
        'order': current_order,
        'employees': employees,
        'today': today,
    })


@login_required
@user_passes_test(is_client, login_url='/accounts/login/')
def remove_from_order(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__client__user=request.user)
    item.delete()
    messages.success(request, "Товар удален из заказа")
    return redirect('current_order')


@login_required
@user_passes_test(is_client, login_url='/accounts/login/')
def confirm_order(request, order_id):
    try:
        client = Client.objects.get(user=request.user)
        current_order = Order.objects.get(id=order_id, client=client)
    except (Client.DoesNotExist, Order.DoesNotExist):
        raise Http404("Заказ не найден или не принадлежит вам")

    if request.method == 'POST':
        # Получаем дату доставки из формы
        delivery_date_str = request.POST.get('delivery_date')
        if delivery_date_str:
            try:
                delivery_date = timezone.datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
                if delivery_date < timezone.now().date():
                    messages.error(request, 'Дата доставки не может быть в прошлом.')
                    return redirect('current_order')
                current_order.delivery_date = delivery_date
            except ValueError:
                messages.error(request, 'Неверный формат даты доставки.')
                return redirect('current_order')

        promo_code = request.POST.get('promo_code', '').strip()
        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code, active=True)
                current_order.promo_code = promo
            except PromoCode.DoesNotExist:
                messages.error(request, 'Недействительный промокод')

        employee_id = request.POST.get('employee_id')
        if employee_id:
            try:
                employee = Employee.objects.get(id=employee_id)
                current_order.employee = employee
            except Employee.DoesNotExist:
                messages.error(request, 'Выбранный сотрудник не найден')

        current_order.status = 'confirmed'
        current_order.save()

        messages.success(request, 'Ваш заказ успешно подтвержден!')
        return redirect('current_order')

    # Если метод не POST — можно сделать редирект или вывести ошибку
    return redirect('current_order')


