from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from datetime import date
import re
from .models import Client, Employee
from .models import Manufacturer
from .models import Review

class ClientRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        label="Номер телефона",
        help_text="Формат: +375 (29) XXX-XX-XX"
    )
    email = forms.EmailField(label="Email")
    date_of_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Формат: ДД.ММ.ГГГГ"
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        pattern = r'^\+375\s\((29|25|33|44)\)\s\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone):
            raise ValidationError(
                "Номер должен быть в формате: +375 (29) XXX-XX-XX"
            )
        return phone

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        if age < 18:
            raise ValidationError(
                "Вы должны быть старше 18 лет для регистрации"
            )
        return date_of_birth



class EmployeeRegistrationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        label="Номер телефона",
        help_text="Формат: +375 (29) XXX-XX-XX"
    )
    email = forms.EmailField(label="Email")
    date_of_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Формат: ДД.ММ.ГГГГ"
    )
    department = forms.CharField(max_length=100, label="Отдел")
    position = forms.CharField(max_length=100, label="Должность", required=False)
    bio = forms.CharField(widget=forms.Textarea, label="Описание работ", required=False)
    photo = forms.ImageField(label="Фото сотрудника", required=False)
    is_visible = forms.BooleanField(label="Отображать на сайте", required=False, initial=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        pattern = r'^\+375\s\((29|25|33|44)\)\s\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone):
            raise ValidationError(
                "Номер должен быть в формате: +375 (29) XXX-XX-XX"
            )
        return phone

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        if age < 18:
            raise ValidationError(
                "Сотрудник должен быть старше 18 лет"
            )
        return date_of_birth

from django import forms
from .models import Manufacturer

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'contact_email', 'address', 'image']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Название',
            'contact_email': 'Контактный email',
            'address': 'Адрес',
            'image': 'Логотип'
        }

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Название',
            'category': 'Категория',
            'price': 'Цена',
            'unit': 'Единица измерения',
            'description': 'Описание',
            'available': 'Доступен',
            'manufacturer': 'Производитель',
            'image': 'Изображение'
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Напишите ваш отзыв здесь...'
            }),
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES)
        }
        labels = {
            'text': 'Текст отзыва',
            'rating': 'Ваша оценка'
        }