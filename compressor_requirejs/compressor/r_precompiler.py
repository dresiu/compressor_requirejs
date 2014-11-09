#!/usr/bin/env python
from __future__ import with_statement
from compressor_requirejs.compiler import RequireJSCompiler


class RequireJSPrecompiler(object):
    """A filter whose output is always the string 'OUTPUT' """

    def __init__(self, content, attrs, filter_type=None, charset=None, filename=None):
        self.content = content
        self.attrs = attrs
        self.filter_type = filter_type
        self.filename = filename
        self.charset = charset
        self.requireJSCompiler = RequireJSCompiler()

    def input(self, **kwargs):
        return self.requireJSCompiler.requirejs(kwargs['basename'], True, False)