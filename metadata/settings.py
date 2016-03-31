from django.conf import settings

METADATA_KEY = getattr(settings, 'METADATA_KEY', 'metadata:%(identifier)s:%(id)s')

REDIS_CONNECTION_CLASS = getattr(settings, 'METADATA_REDIS_CONNECTION_CLASS', None)

REDIS_CONNECTION = getattr(settings, 'METADATA_REDIS_CONNECTION', {})

DEFAULT_TIMEOUT = getattr(settings, 'METADATA_DEFAULT_TIMEOUT', None)
