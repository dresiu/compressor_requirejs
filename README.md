Introduction
============

This module ables django compressor to compile requirejs files info one or a few bigger files using r.js.

Features:
---------
* compiling plenty of files into one file
* making a few compiled files for splitting functionality
* all features of django compressor i.e.:
    * caching files,
    * adding hashes,
    * processing with django template markup,
    * post compiling
* tracing build files for modification (caching results)


Requirements
============

* Django >= 1.5
* django_compressor >= 1.3
* PyExecJs 1.0.4

* node js

Installation
============

1. Add ``compressor_requirejs`` to installed apps
2. Setup ``django_compressor`` properties for working with django compressor
3. Setup ``compressor_requirejs``:
    * Set ``COMPRESS_PRECOMPILERS`` of django compressor for using with standard markup in compress tags
    * Set ``CACHE`` backends for django compressor and requirejs plugin, recomended for development
        is ``'default'`` with ``DummyCache`` and ``'locmem'`` with ``LocMemCache``
    * Set ``COMPRESSOR_REQUIREJS_TMP`` to a custom **existing** temporary directory path


```python
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
```

Advanced configuration
======================

```python

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
```

Using
=====

Prepare at least two js files, one build file and one module file:

###build.js

```javascript
({
    baseUrl: '.',
    name: 'main'
})
```

###main.js
```javascript
require([], function () {
    console.log('wow, its working');
});
```

Put those files in static directory of your app.
``build.js`` pointing to ``main.js`` with ``name`` attribute, so launching build file compile ``main.js`` with other dependencies.

Django template configuration
-----------------------------
```HTML+Django
{% compress js %}
    <script type="text/requirejs" src="{{ STATIC_URL }}mainapp/js/build.js"></script>
{% endcompress %}
```

Of course you have to include ``require.js`` file, ex:

```HTML+Django
{% compress js %}
   <script src="{{ STATIC_URL }}mainapp/js/require.js"></script>
{% endcompress %}
```

Advanced features
=================

You can use django template language tags in your js files.
It can be processed with django compressor's template processors but there is a hack to omit this markup during requirejs compilation.

```javascript
//>startExclusion
var importantVariableExcludedDuringCompilationButVisibleInRenderedFile = {{ PROJECT_VARIABLE }};
//>endExclusion
```

Those tags are used to exclude fragment of code (commenting it) during requirejs compilation,
and after compilation it will be available, and can be processed by django compressor.

Also you can use tags in string without above markup:
```javascript
var x = '{{ STATIC_URL }}/path/';
```
