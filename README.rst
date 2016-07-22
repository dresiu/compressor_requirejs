v1.5
====
- license changed to the MIT

v1.4
====

- support for python 3.4
- support for django 1.9.x
- support for django-compressor up to 1.6 (2.0 not officially supported but may work in some circumstances)
- support for utf8 encoding in files (required encoding)

v1.3
====

- install_requires added,
- support for django compressor 1.4 precompiler constructor

v1.2
====

- invalidate cache on compiling error,
- support for custom logging


Introduction
============

This module ables django compressor to compile requirejs files into one
or a few bigger files using r.js.

Features:
---------

-  compiling plenty of files into one file
-  making a few compiled files for splitting functionality
-  all features of django compressor i.e.:

   -  caching files,
   -  adding hashes,
   -  processing with django template markup,
   -  post compiling

-  tracing build files for modification (caching results)

Requirements
============

-  Django >= 1.6
-  django\_compressor >= 1.3 and < 2.0
-  PyExecJs >= 1.1.0

-  node js

Installation
============

1. Add ``compressor_requirejs`` to installed apps
2. Setup ``django_compressor`` properties for working with django
   compressor
3. Setup ``compressor_requirejs``:

   -  Set ``COMPRESS_PRECOMPILERS`` of django compressor for using with
      standard markup in compress tags
   -  Set ``CACHE`` backends for django compressor and requirejs plugin,
      recomended for development is ``'default'`` with ``DummyCache``
      and ``'locmem'`` with ``LocMemCache``
   -  Set ``COMPRESSOR_REQUIREJS_TMP`` to a custom **existing**
      temporary directory path

.. code:: python

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        },
        'locmem': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }

    COMPRESS_PRECOMPILERS = (
        ('text/requirejs', 'compressor_requirejs.compressor.r_precompiler.RequireJSPrecompiler'),
    )

    COMPRESSOR_REQUIREJS_TMP = django_project_path_join('tmp')

Advanced configuration
======================

.. code:: python


        #COMPRESSOR_REQUIREJS config

        #absolute path to r.js
        #default: path in resources of this package
        COMPRESSOR_REQUIREJS_R_JS = 'path/to/r.js'

        #absolute path to temporary directory
        COMPRESSOR_REQUIREJS_TMP = '/tmp'

        #path to global configuration for requirejs bulid aka 'mainConfigFile' in r.js configuration
        # WARNING setting this path overwrites built in global config of this plugin and some feature can not working
        COMPRESSOR_REQUIREJS_GLOBAL_CONFIG = 'path/to/global/requirejs/config.js'

        #setup compressor_requirejs caching backend, preferred local memory backend mainly for development,
        #backend should be configured in django CACHE configuration
        #default: 'locmem'
        COMPRESSOR_REQUIREJS_CACHE_BACKEND = 'locmem'

        #timeout for caching results in cache (in seconds)
        #default: 3600
        COMPRESSOR_REQUIREJS_CACHE_TIMEOUT = 3600

        #node js executable path, it is preferred to have mapped 'node' in your PATH
        #default: node
        COMPRESSOR_REQUIREJS_NODE_EXECUTABLE = 'node'

        #setup custom logging function for output
        def logging_compressor_requirejs(text):
            import logging
            logger = logging.getLogger('mainapp.custom')
            logger.debug(text)

        COMPRESSOR_REQUIREJS_LOGGING_OUTPUT_FUNCTION = logging_compressor_requirejs


Using
=====

Prepare at least two js files, one build file and one module file:

build.js
--------

.. code:: javascript

    ({
        baseUrl: '.',
        name: 'main'
    })

main.js
-------

.. code:: javascript

    require([], function () {
        console.log('wow, its working');
    });

Put those files in static directory of your app. ``build.js`` pointing
to ``main.js`` with ``name`` attribute, so launching build file compile
``main.js`` with other dependencies.

Django template configuration
-----------------------------

::

     {% compress js %}
          <script type="text/requirejs" src="{{ STATIC_URL }}mainapp/js/build.js"></script>
     {% endcompress %}

Of course you have to include ``require.js`` file, ex:

::

    {% compress js %}
        <script src="{{ STATIC_URL }}mainapp/js/require.js"></script>
    {% endcompress %}

Advanced features
=================

You can use django template language tags in your js files. It can be
processed with django compressor's template processors but there is a
hack to omit this markup during requirejs compilation.

.. code:: javascript

    //>startExclusion
    var importantVariableExcludedDuringCompilationButVisibleInRenderedFile = {{ PROJECT_VARIABLE }};
    //>endExclusion

Those tags are used to exclude fragment of code (commenting it) during
requirejs compilation, and after compilation it will be available, and
can be processed by django compressor.

Also you can use tags in string without above markup:

.. code:: javascript

    var x = '{{ STATIC_URL }}/path/';


Global js library mappings
--------------------------

You can use global path mappings for javascript files,
for example if you have a few apps in project and one handle main libraries simply add them to global paths.

.. code:: python

    COMPRESSOR_REQUIREJS_REQUIRED_LIBS = {}

In django object simply type key value elements, where key is valid path mapping and value is path to js file.

**IMPORTANT**

- mapping name can be only solid string without dots eg.: ``mapping_for_path`` not ``mapping.for.path``
- path can be relative to current project and will be processed with defined static file finder


.. code:: python

    COMPRESSOR_REQUIREJS_REQUIRED_LIBS = {
        'jquery': 'mainapp/js/libs/jquery-2.1.0.min.js'
    }
