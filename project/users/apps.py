from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # connect the signal reciever (in users/signals.py) to the app
    def ready(self):
        import users.signals
        