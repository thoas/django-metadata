from . import settings
from .utils import get_client


client = get_client(settings.REDIS_CONNECTION,
                    connection_class=settings.REDIS_CONNECTION_CLASS)
