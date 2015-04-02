import six


class MetadataContainer(object):
    def __init__(self, connection, key, instance=None):
        self._connection = connection
        self._key = key
        self.loaded = False
        self.instance = instance

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

    def __set__(self, instance, metadata):
        to_update = dict((key, value)
                         for key, value in six.iteritems(metadata)
                         if value is not None)

        to_delete = [k for k, v in six.iteritems(metadata)
                     if v is None]

        container = self.__get__(instance)

        redis = container.connection

        if to_delete:
            redis = redis.pipeline()

        if to_update:
            redis.hmset(container.key, to_update)

        if to_delete:
            for key in to_delete:
                redis.hdel(container.key, key)

            redis.execute()

        container.reload()

        return container

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

    def __delitem__(self, key):
        self.connection.hdel(self.key, key)

    def __getitem__(self, key):
        if key in self.metadata:
            return self.metadata[key]

        raise KeyError

    def __setitem__(self, key, value=None):
        if value is None:
            self.connection.hdel(self.key, key)
        else:
            self.connection.hset(self.key, key, value)

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
