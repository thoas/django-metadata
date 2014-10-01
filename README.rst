django-metadata
===============

Attach metadata to any Django models using redis.

.. image:: https://secure.travis-ci.org/thoas/django-metadata.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/django-metadata

Compatibility
-------------

This library is compatible with:

- python2.6, django1.5
- python2.6, django1.6
- python2.7, django1.5
- python2.7, django1.6
- python2.7, django1.7
- python3.3, django1.5
- python3.3, django1.6
- python3.3, django1.7
- python3.4, django1.5
- python3.4, django1.6
- python3.4, django1.7

Installation
------------

1. Either check out the package from GitHub_ or it pull from a release via PyPI ::

       pip install django-metadata

Usage
-----

With ``django-metadata`` you can attach metadata to any Django models.

Currently only Redis_ is supported with only redis-py_ as backend.

Let's say you have this model: ::

    # models.py

    from django.db import models

    class User(models.Model):
        username = models.Charfield(max_length=150)

Now you have to attach the ``MetadataMixin`` to your model ::

    # models.py

    from django.db import models

    from metadata.mixins import MetadataMixin

    class User(MetadataMixin, models.Model):
        username = models.Charfield(max_length=150)

You can customize the way ``django-metadata`` is storing your values by providing
a ``metadata_key`` property to your model ::

    # models.py

    from django.db import models

    from metadata.mixins import MetadataMixin

    class User(MetadataMixin, models.Model):
        username = models.Charfield(max_length=150)

        def metadata_key(self):
            return 'metadata:utilisateur:%d' % self.pk


By default, the schema will be ``metadata:%(lowerclassname)s:%(primary_key)s``.

Now we have connected our model to the mixin we can play with the API.

The API of ``MetadataContainer`` follows the same principes as ``dict``.

Adding keys
...........

::

    In [1]: from myapp.models import User

    In [2]: user = User.objects.create(username='thoas')

    In [3]: user.metadata['key'] = 'value'

    In [4]: user = User.objects.get(username='thoas')

    In [5]: user.metadata['key']
    value

    In [6]: user.metadata = {'key': 'value1'}

    In [7]: user.metadata['key']
    value1


Removing keys
.............

You can either removing a key by setting its value to ``None`` or use the ``del``
operator.

::

    In [8]: del user.metadata['key']

    In [9]: user.metadata['key'] # will raises a KeyError

    In [10]: user.metadata.get('key', None)
    None

    In [11]: user.metadata['value'] = 'key'

    In [12]: user.metadata['value'] = None

    In [13]: user.metadata['value'] # will raises a KeyError

    In [14]: user.metadata.get('key', None)
    None

    In [15]: user.metadata['value'] = 'key'

    In [16]: user.metadata['foo'] = 'bar'

    In [17]: user.metadata = {'foo': None}

    In [18]: user.metadata['foo'] # will raises a KeyError

    In [19]: user.metadata['value']
    key

Iterating keys
..............

::

    In [20]: 'value' in user.metadata
    True

    In [21]: user.metadata.values()
    ['key']

    In [22]: user.metadata.keys()
    ['value']

    In [23]: user.metadata.items()
    [('value', 'key')]

Incrementing keys
.................

As we are using Redis as storing engine you can use some of its nice features ::

    In [24]: user.metadata.incr('counter')

    In [25]: user.metadata['counter']
    1

    In [26]: user.metadata.incr('counter', 2)

    In [27]: user.metadata['counter']
    3

Inspiration
-----------

``django-metadata`` comes from an original idea of twidi_.

.. _GitHub: https://github.com/thoas/django-metadata
.. _redis-py: https://github.com/andymccurdy/redis-py
.. _Redis: http://redis.io/
.. _twidi: https://github.com/twidi
