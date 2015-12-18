django-metadata
===============

Attach metadata to any Django models using redis.

.. image:: https://secure.travis-ci.org/thoas/django-metadata.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/thoas/django-metadata

Installation
------------

Either check out the package from GitHub_ or it pull from a release via PyPI::

       pip install django-metadata

Usage
-----

With ``django-metadata`` you can attach metadata to any Django models, you will
be able to link keys and theirs values to any instances.

Currently only Redis_ is supported with only redis-py_ as backend.

Let's say you have this model:

.. code-block:: python

    # models.py

    from django.db import models

    class User(models.Model):
        username = models.CharField(max_length=150)

Now you have to attach the ``MetadataMixin`` to your model:

.. code-block:: python

    # models.py

    from django.db import models

    from metadata.mixins import MetadataMixin

    class User(MetadataMixin, models.Model):
        username = models.CharField(max_length=150)


You can customize the way ``django-metadata`` is storing your values by providing
a ``metadata_key`` property to your model:

.. code-block:: python

    # models.py

    from django.db import models

    from metadata.mixins import MetadataMixin

    class User(MetadataMixin, models.Model):
        username = models.CharField(max_length=150)

        def metadata_key(self):
            return 'metadata:utilisateur:%d' % self.pk


By default, the schema will be ``metadata:%(lowerclassname)s:%(primary_key)s``.

Now we have connected our model to the mixin we can play with the API.

The API of ``MetadataContainer`` follows the same principes as ``dict``.

Adding keys
...........

.. code-block:: python

    >>> from myapp.models import User
    >>> user = User.objects.create(username='thoas')
    >>> user.metadata['mail_signup_sent'] = 1
    >>> user = User.objects.get(username='thoas')
    >>> user.metadata['mail_signup_sent']
    1
    >>> user.metadata = {'mail_signup_sent': 0}
    >>> user.metadata['mail_signup_sent']
    0


Removing keys
.............

You can either removing a key by setting its value to ``None`` or use the ``del``
operator.

.. code-block:: python

    >>> del user.metadata['key']
    >>> user.metadata['key']
    Traceback (most recent call last):
        ...
    KeyError: 'key'
    >>> user.metadata.get('key', None)
    None
    >>> user.metadata['foo'] = 'bar'
    >>> user.metadata['foo'] = None
    >>> user.metadata['foo']
    Traceback (most recent call last):
        ...
    KeyError: 'foo'
    >>> user.metadata.get('foo', None)
    None
    >>> user.metadata['key'] = 'value'
    >>> user.metadata['foo'] = 'bar'
    >>> user.metadata = {'foo': None}
    >>> user.metadata['foo']
    Traceback (most recent call last):
        ...
    KeyError: 'foo'
    >>> user.metadata['key']
    value

Iterating keys
..............

.. code-block:: python

    >>> 'value' in user.metadata
    True
    >>> user.metadata.values()
    ['value']
    >>> user.metadata.keys()
    ['key']
    >>> user.metadata.items()
    [('key', 'value')]

Incrementing keys
.................

As we are using Redis as storing engine you can use some of its nice features:

.. code-block:: python

    >>> user.metadata.incr('counter')
    >>> user.metadata['counter']
    1
    >>> user.metadata.incr('counter', 2)
    >>> user.metadata['counter']
    3

Inspiration
-----------

``django-metadata`` comes from an original idea of twidi_.

.. _GitHub: https://github.com/thoas/django-metadata
.. _redis-py: https://github.com/andymccurdy/redis-py
.. _Redis: http://redis.io/
.. _twidi: https://github.com/twidi
