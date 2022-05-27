"""
This is simplest possible kernel for dg based on echokernel.
"""

import errno
import os
import signal
import subprocess
import sys
import dg
import re
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import urllib, base64

from ipykernel.kernelbase import Kernel

import io
from contextlib import redirect_stdout

class IdgKernel(Kernel):
    """
    Idg: jupyter kernel for dg
    """
    implementation = 'Idg'
    implementation_version = '1.0'
    language = 'dg'
    language_version = '1.1.0' #??
    language_info = {
        'name': 'Dg',
        'mimetype': 'text/dg',
        'file_extension': '.dg',
        'codemirror_mode': {
            'name': 'python'
        },
        'pygments_lexer': 'ipython3'
    }
    banner = "Idg kernel - awesomeness exceeds all limit!"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eval_("import '/dg/types'")
        self.eval_("import '/dg/builtins'")
        #self.eval_("")
        self.eval_("import '/dg/add_module_builtins'")
        self.eval_("module = sys.modules !! '__main__' = types.ModuleType '__main__'")
        self.eval_("add_module_builtins (sys.modules !! '__main__')")
        self.eval_("add_module_builtins module")

        # initializing dg repl:
        # -this project will be shared among all kernels
        # +will do bro!

    def eval_(self, code_, module_ = None):
        if module_ is None:
            return eval(dg.compile(code_, '<file>'))
        else:
            return eval(dg.compile(code_, '<file>'), module_.__dict__)

    def _to_png(self, fig_):
        """Return a base64-encoded PNG from a
        matplotlib figure."""
        imgdata_ = BytesIO()
        fig_.savefig(imgdata_, format='png')
        imgdata_.seek(0)
        return urllib.parse.quote(
            base64.b64encode(imgdata_.getvalue()))

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            code = re.sub(r'^\%.*\n?', '', code, flags=re.MULTILINE)

            errorflag_ = False
            f = io.StringIO()
            with redirect_stdout(f):
                try:
                    eval_ = self.eval_(code, module)
                except (RuntimeError, TypeError, NameError, AttributeError, ValueError) as e:
                    errorflag_ = True
                    eval_ = str(e)

                std_out_ = f.getvalue()

            ret_ = ''
            if len(std_out_) > 0:
                ret_ = str(std_out_) + '\n'

            if eval_ is not None:
                ret_ = ret_ + str(eval_)

            if isinstance(eval_, matplotlib.figure.Figure):
                png_ = self._to_png(eval_)
                content_ = {
                    'source': 'kernel',
                    'data': {
                        'image/png': png_
                    },
                    'metadata' : {
                        'image/png' : {
                            'width': 600,
                            'height': 400
                        }
                    }
                }
                self.send_response(self.iopub_socket,
                                   'display_data', content_)

            stream_content = {'name': 'stderr' if errorflag_ else 'stdout',
                              'text': ret_}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        finaldata_ = {
            'status': 'error' if errorflag_ else 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

        return finaldata_
