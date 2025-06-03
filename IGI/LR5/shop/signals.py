from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Фиксирует время входа пользователя."""
    try:
        from .models import UserVisit  # Ленивый импорт внутри функции
        with transaction.atomic():
            UserVisit.objects.create(
                user=user,
                session_key=request.session.session_key,
            )
    except Exception as e:
        print(f"Ошибка при создании UserVisit: {e}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Фиксирует время выхода пользователя."""
    try:
        from .models import UserVisit  # Ленивый импорт внутри функции
        with transaction.atomic():
            last_visit = UserVisit.objects.filter(
                user=user,
                session_key=request.session.session_key,
                logout_time__isnull=True
            ).last()
            if last_visit:
                last_visit.logout_time = timezone.now()
                last_visit.save()
    except Exception as e:
        print(f"Ошибка при обновлении UserVisit: {e}")