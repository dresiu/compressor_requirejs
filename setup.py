from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='compressor_requirejs',
    packages=['compressor_requirejs',
              'compressor_requirejs.compressor'],
    package_data = {
        "compressor_requirejs": [
            "resources/*.js"
        ],
    },
    version='1.1',
    description='Library for django compressor, which helps to build requirejs',
    long_description=read('README.rst'),
    author='Andrzej Przybyszewski',
    author_email='mcendrju@gmail.com',
    url='https://github.com/dresiu/compressor_requirejs',
    download_url='https://github.com/dresiu/compressor_requirejs/tarball/1.1',
    keywords=['compressor_requirejs', 'django_compressor', 'django', 'compressor', 'requirejs'],
    requires=['django_compressor', 'PyExecJs'],
    classifiers=["Environment :: Web Environment",
                 "Framework :: Django",
                 "Intended Audience :: Developers",
                 "Programming Language :: Python :: 2.7"],
)