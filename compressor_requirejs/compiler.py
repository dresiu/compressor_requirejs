import codecs
import subprocess
import os
import sys

from django.core.exceptions import ImproperlyConfigured
from django.contrib.staticfiles import finders
import execjs

from .config import settings

try:
    from django.core.cache import caches

    def get_cache(name):
        return caches[name]
except ImportError:
    from django.core.cache import get_cache


APP_NAME = 'compressor_requirejs'


def current_exc_type():
    return sys.exc_info()[0]


class RequireJSCompilerException(Exception):
    pass


class RequireJSCompiler(object):
    def __init__(self):
        self.r = getattr(settings, 'COMPRESSOR_REQUIREJS_R_JS', None)
        if not self.r:
            raise ImproperlyConfigured('COMPRESSOR_REQUIREJS_R_JS not set')
        self.tmp = getattr(settings, 'COMPRESSOR_REQUIREJS_TMP', None)
        if not self.tmp:
            raise ImproperlyConfigured('COMPRESSOR_REQUIREJS_TMP not set')

        self.libs = self.required_libs()
        self.global_config = getattr(settings, 'COMPRESSOR_REQUIREJS_GLOBAL_CONFIG', None)
        self.global_preconfig = getattr(settings, 'COMPRESSOR_REQUIREJS_GLOBAL_PRECONFIG', None)
        self.printf = settings.COMPRESSOR_REQUIREJS_LOGGING_OUTPUT_FUNCTION

    def get_fullpath(self, path, resolve_path=True):
        if os.path.isabs(path):
            return path
        if not resolve_path:
            return path
        files = finders.find(path, all=True)
        if isinstance(files, list):
            if len(files) > 0:
                return files[0]
            else:
                return path
        elif files is not None:
            return files
        else:
            return path

    def required_libs(self):
        paths = []
        if hasattr(settings, 'COMPRESSOR_REQUIREJS_REQUIRED_LIBS'):
            for arg in settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS.keys():
                path = self.get_fullpath(settings.COMPRESSOR_REQUIREJS_REQUIRED_LIBS[arg])
                if path.endswith('.js'):
                    path = path[:-3]
                paths.append('paths.%s=%s' % (arg, path))
        return paths

    def _tmp_file_gen(self, filename, postfix):
        return os.path.join(self.tmp, filename.replace('\\', '_').replace('/', '_').replace('.', '_') + postfix)

    def requirejs(self, filename, resolve_path=True, include_tags=True):
        outfile = self._tmp_file_gen(filename, '_build.js')
        build_filename = self.get_fullpath(filename, resolve_path)
        #check cache
        c = CacheFilesAccess(build_filename, outfile)

        if not c.validate():
            self.printf('[%s] cache invalid, compiling: %s' % (APP_NAME, filename))
            process_args = [settings.COMPRESSOR_REQUIREJS_NODE_EXECUTABLE,
                            self.r,
                            '-o', build_filename,
                            'out=' + outfile]
            process_args += self.libs
            if self.global_config:
                process_args.append('mainConfigFile=' + self.get_fullpath(self.global_config))
            else:
                process_args.append('mainConfigFile=' + self.global_preconfig)
            try:
                output = subprocess.check_output(process_args)
                c.do_caching(output, self.get_fullpath(self.global_config) if self.global_config else None)
            except current_exc_type() as e:
                c.invalidate()
                if hasattr(e, 'output'):
                    raise RequireJSCompilerException(e.output.decode('utf-8'))
                raise e
            if u'Error' in output.decode('utf-8'):
                c.invalidate()
                raise RequireJSCompilerException(output.decode('utf-8'))
        else:
            self.printf('[%s] skipping compilation: %s' % (APP_NAME, filename))

        f = codecs.open(outfile, 'r', 'utf-8')
        ret = '<script>%s</script>' % f.read() if include_tags else f.read()
        f.close()
        return ret

    def requirejs_dir(self, filename, dirpath, resolve_path=True):
        build_filename = self.get_fullpath(filename, resolve_path)
        process_args = [settings.COMPRESSOR_REQUIREJS_NODE_EXECUTABLE,
                        self.r,
                        '-o', build_filename,
                        'dir=' + dirpath]
        process_args += self.libs
        if self.global_config:
            process_args.append('mainConfigFile=' + self.get_fullpath(self.global_config))
        else:
            process_args.append('mainConfigFile=' + self.global_preconfig)
        try:
            output = subprocess.check_output(process_args)
        except current_exc_type() as e:
            if hasattr(e, 'output'):
                raise RequireJSCompilerException(e.output.decode('utf-8'))
            raise e
        if u'Error' in output:
            raise RequireJSCompilerException(output.decode('utf-8'))


class CacheFileModel(object):
    modified_time = ''
    filename = ''

    def __unicode__(self):
        return '%s %s' % (self.modified_time, self.filename)


class CacheFilesAccess(object):
    PATH_SPLIT = '/'

    MODULE_PATH_SPLIT = '!'

    def __init__(self, build_file, output_file):
        self.cache = get_cache(settings.COMPRESSOR_REQUIREJS_CACHE_BACKEND)
        self.build_file = build_file
        self.output_file = output_file
        self.cache_timeout = settings.COMPRESSOR_REQUIREJS_CACHE_TIMEOUT
        self.base_path = self._get_build_base_url()

    def _cache_hash_gen(self, module_file):
        return self.output_file + '::' + module_file

    def do_caching(self, output, global_config):
        module_files = self._get_files(output)
        files_dict = dict()
        if global_config is not None:
            module_files += [global_config]

        for module in module_files:
            if os.path.exists(module):
                cm = CacheFileModel()
                cm.filename = module
                cm.modified_time = os.path.getmtime(module)
                files_dict[module] = cm
        self.cache.set(self._cache_hash_gen(''), files_dict, self.cache_timeout)

    def validate(self):
        files = self.cache.get(self._cache_hash_gen(''))
        if not files:
            return False
        files = files.values()
        for file_model in files:
            if os.path.exists(file_model.filename):
                if file_model.modified_time != os.path.getmtime(file_model.filename):
                    return False
            else:
                return False
        return True

    def invalidate(self):
        self.cache.delete(self._cache_hash_gen(''))

    def _get_files(self, output):
        lines = output.decode('utf-8').split(u'\n')
        module_files = [self.build_file] + lines
        return [self._normalize(m) for m in module_files if os.path.isfile(m) or self.MODULE_PATH_SPLIT in m]

    def _normalize(self, file_path):
        if self.MODULE_PATH_SPLIT in file_path:
            relative_path = file_path.split(self.MODULE_PATH_SPLIT)[1]
            return os.path.normpath(os.path.join(self.base_path, *relative_path.split(self.PATH_SPLIT)))
        else:
            return os.path.normpath(file_path)

    def _get_build_base_url(self):
        runtime = execjs.get('Node')
        runtime._command = settings.COMPRESSOR_REQUIREJS_NODE_EXECUTABLE
        ctx = runtime.eval(open(self.build_file, 'r').read())
        return os.path.join(os.path.dirname(self.build_file), *ctx.get('baseUrl', '').split(self.PATH_SPLIT))
