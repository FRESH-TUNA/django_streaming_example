from django.apps import AppConfig

class AuthConfig(AppConfig):
    # name is app folder name
    name = 'auth'

    # label is unique seperator on database
    label = 'streaming_example-auth'
