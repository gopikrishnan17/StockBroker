from django.apps import AppConfig
from multiprocessing import Process
import threading

class BuystocksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "buystocks"
    def ready(self):
        import buystocks.signals
        from buystocks.tasks import check_and_execute_orders
        orderThread = threading.Thread(target=check_and_execute_orders, daemon = True)
        orderThread.start()
