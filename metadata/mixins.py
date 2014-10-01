from .models import MetadataContainer

from . import settings
from .connection import client


class MetadataMixin(object):
    metadata = MetadataContainer(connection=client,
                                 key=lambda instance: instance.metadata_key)

    @property
    def metadata_key(self):
        key = getattr(self, 'METADATA_KEY', settings.METADATA_KEY)

        if key:
            return key % {
                'identifier': self.__class__.__name__.lower(),
                'id': self.pk
            }

        return None
