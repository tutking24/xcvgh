Caching with IGitt
==================

IGitt provides a default in-memory cache to store data from requests to reuse
and avoid the problems of rate limiting. To use your own cache store, please
refer below.

Django
------

Configure your Django application settings providing the cache backend of your
choice. Choose your cache backend from `the list of available backends for
Django <https://docs.djangoproject.com/en/1.11/ref/settings/#caches>`_.

An example configuration can be found below.

.. code-block:: python

    # settings.py
    ...

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'igitt_cache',
            'TIMEOUT': 60*60*24*7*4,  # 4 weeks
            'OPTIONS': {'MAX_ENTRIES': 10 ** 9}  # 1 trillion entries
        }
    }


Once you've configured cache backend with Django, proceed forward and connect
IGitt's caching mechanism within the chosen cache backend. Make sure that you
**do this as soon as the app is ready to use the database**. In your main
application's ``AppConfig``, implement the ``ready`` method as follows.

.. code-block:: python

    # apps.py
    from django.apps import AppConfig
    from django.core.cache import cache as django_cache
    from IGitt.Utils import Cache


    class ExampleConfig(AppConfig):
        ...

        def ready(self):
            # Initialize the IGitt Cache management.
            Cache.use(django_cache.get, django_cache.set)


If you've chosen a ``DatabaseCache`` backend, before you start your application,
create the database table by running the following.::

    python manage.py createcachetable


Flask
-----

Flask itself does not provide support for caching like Django does, but
Werkzeug, one of the libraries it is based on, has some very basic cache
support. It supports multiple cache backends like Django does. For more details
please refer `here <http://werkzeug.pocoo.org/docs/0.14/contrib/cache/#module-werkzeug.contrib.cache>`_.

Create a cache object once and keep it around, similar to how other Flask
objects are created. This cache also provides, simple to use, ``set`` and
``get`` methods to store and retrieve objects respectively. Now that your cache
is properly configured, please connect IGitt's caching mechanism to your cache
object **as soon as it is created**. A sample code is given below.::

    from werkzeug.contrib.cache import RedisCache
    from IGitt.Utils use Cache

    flask_cache = RedisCache(key_prefix='igitt_cache')
    Cache.use(flask_cache.get, flask_cache.set)

You are now ready to use IGitt caching mechanism with your flask application.
The same approach can be used with any other applications alike.
