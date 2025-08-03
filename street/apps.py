from django.apps import AppConfig


class StreetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'street'

def ready(self): 
    import street.signals # Replace 'yourapp' with your actual app name 

