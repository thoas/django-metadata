import six

from fnmatch import fnmatch

from . import compat, settings


class MetadataContainer(object):
    def __init__(self, connection, key, instance=None, default_timeout=settings.DEFAULT_TIMEOUT):
        self._connection = connection
        self._key = key
        self.loaded = False
        self.instance = instance
        self.default_timeout = default_timeout

    @property
    def metadata(self):
        if not self.loaded:
            self.reload()

        return self._metadata

    @property
    def key(self):
        if callable(self._key):
            return self._key(self.instance)

        return self._key

    @property
    def connection(self):
        if callable(self._connection):
            return self._connection(self.instance)

        return self._connection

    def __get__(self, instance, owner=None):
        if instance:
            return self.copy(instance=instance)

        return self

    def get_timeout(self, timeout):
        if timeout is compat.DEFAULT_TIMEOUT:
            timeout = self.default_timeout

        if timeout is not None:
            timeout = int(timeout)

        return timeout

    def __set__(self, instance, metadata):
        container = self.__get__(instance)
        container.set(metadata)
        container.reload()

        return container

    def set(self, metadata, timeout=compat.DEFAULT_TIMEOUT):
        to_update = dict((key, value)
                         for key, value in six.iteritems(metadata)
                         if value is not None)

        to_delete = [k for k, v in six.iteritems(metadata)
                     if v is None]

        hash_key = self.key

        exists = self.connection.exists(hash_key)

        with self.connection.pipeline() as pipe:
            if to_update:
                pipe.hmset(hash_key, to_update)

            if to_delete:
                for key in to_delete:
                    pipe.hdel(hash_key, key)

            timeout = self.get_timeout(timeout)

            if not exists and timeout:
                pipe.expire(hash_key, timeout)

            pipe.execute()

    def get_or_set(self, key, func):
        value = self.get(key)

        if value is None:
            value = func()

            self[key] = value

        return value

    def reload(self):
        self._metadata = self.connection.hgetall(self.key) or {}

    def incr(self, key, incrby=1):
        return self.connection.hincrby(self.key, key, incrby)

    def listkeys(self, key):
        keys = [key, ]

        if '*' in key:
            keys = [result
                    for result in self.connection.hkeys(self.key)
                    if fnmatch(result, key)]

        return keys

    def __delitem__(self, key):
        with self.connection.pipeline() as pipe:
            for key in self.listkeys(key):
                pipe.hdel(self.key, key)

            pipe.execute()

    def __getitem__(self, key):
        if key in self.metadata:
            return self.metadata[key]

        raise KeyError

    def __setitem__(self, key, value=None):
        self.set({key: value})

    def __copy__(self, instance=None):
        return self.__class__(self._connection,
                              self._key,
                              instance=instance or self.instance)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def iteritems(self):
        for item in self.metadata.items():
            yield item

    def iterkeys(self):
        for k, v in self.iteritems():
            yield k

    def itervalues(self):
        for k, v in self.iteritems():
            yield v

    def items(self):
        return list(self.iteritems())

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def has_key(self, key):
        return key in self.metadata

    __contains__ = has_key
    __iter__ = iterkeys

    def copy(self, instance=None):
        return self.__copy__(instance=instance)

    def __str__(self):
        return str(dict(self.items()))
