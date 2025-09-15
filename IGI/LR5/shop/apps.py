from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        try:
            from django.db import connection
            if 'shop_uservisit' in connection.introspection.table_names():
                import shop.signals
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error loading signals: {e}")