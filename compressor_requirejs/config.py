from os.path import dirname, abspath, join

from django.conf import settings as django_settings


THIS_PATH = dirname(abspath(__file__))


class LazySettings(object):
    @property
    def COMPRESSOR_REQUIREJS_R_JS(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_R_JS", join(THIS_PATH, join('resources', 'r.js')))

    @property
    def COMPRESSOR_REQUIREJS_TMP(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_TMP", join(THIS_PATH, 'tmp'))

    @property
    def COMPRESSOR_REQUIREJS_GLOBAL_PRECONFIG(self):
        return join(THIS_PATH, join('resources', 'global_config.js'))

    @property
    def COMPRESSOR_REQUIREJS_GLOBAL_CONFIG(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_GLOBAL_CONFIG", None)

    @property
    def COMPRESSOR_REQUIREJS_CACHE_BACKEND(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_CACHE_BACKEND", 'locmem')

    @property
    def COMPRESSOR_REQUIREJS_CACHE_TIMEOUT(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_CACHE_TIMEOUT", 60 * 60)

    @property
    def COMPRESSOR_REQUIREJS_NODE_EXECUTABLE(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_NODE_EXECUTABLE", 'node')

    @property
    def COMPRESSOR_REQUIREJS_REQUIRED_LIBS(self):
        return getattr(django_settings, "COMPRESSOR_REQUIREJS_REQUIRED_LIBS", {})


settings = LazySettings()
