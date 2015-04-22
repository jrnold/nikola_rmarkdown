# -*- coding: utf-8 -*-

# Copyright © 2015 Jeffrey Arnold

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Implementation of compile_html based on R Markdown

You will need, of course, to install R and the R package rmarkdown.

"""

import codecs
import os
import subprocess

from rpy2.robjects.packages import importr

from nikola.plugin_categories import PageCompiler
from nikola.utils import makedirs, req_missing, write_metadata

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict  # NOQA


class CompileRMarkdown(PageCompiler):
    """Compile R Markdown into HTML."""

    name = "rmarkdown"
    demote_headers = True

    def compile_html(self, source, dest, is_two_file=True):
        makedirs(os.path.dirname(dest))
        r_rmarkdown = importr("rmarkdown")
        r_base = importr("base")
        r_rmarkdown.render(source,
                           output_file = os.path.join(os.getcwd(), dest),
                           runtime = "static",
                           output_format = "html_fragment",
                           clean = True,
                           quiet = True)

    def create_post(self, path, **kw):
        content = kw.pop('content', None)
        onefile = kw.pop('onefile', False)
        # is_page is not used by create_post as of now.
        kw.pop('is_page', False)
        metadata = {}
        metadata.update(self.default_metadata)
        metadata.update(kw)
        makedirs(os.path.dirname(path))
        if not content.endswith('\n'):
            content += '\n'
        with io.open(path, "w+", encoding="utf8") as fd:
            if onefile:
                fd.write('<!--\n')
                fd.write(write_metadata(metadata))
                fd.write('-->\n\n')
            fd.write(content)
