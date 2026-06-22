from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'
    def ready(self):
        # Import signal handlers to keep dealership ratings in sync
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
