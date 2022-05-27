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
            'name': 'haskell'
        },
        'pygments_lexer': 'haskell'
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

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            code = re.sub(r'^\%.*\n?', '', code, flags=re.MULTILINE)

            f = io.StringIO()
            with redirect_stdout(f):
                eval_ = self.eval_(code, module)
                std_out_ = f.getvalue()

            ret_ = ''
            if len(std_out_) > 0:
                ret_ = str(std_out_) + '\n'

            if eval_ is None:
                ret_ = ret_ + str(eval_)

            stream_content = {'name': 'stdout',
                              'text': ret_}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
