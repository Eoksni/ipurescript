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
import IPython

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
        self.eval_("import '/dg/BUILTINS'")
        self.eval_("Compiler = import '/dg/Compiler'")
        #self.eval_("")
        self.eval_("import '/dg/add_module_builtins'")
        self.eval_("module = sys.modules !! '__main__' = types.ModuleType '__main__'")
        self.eval_("add_module_builtins (sys.modules !! '__main__')")
        self.eval_("add_module_builtins module")
        #self.eval_("completion_ns = globals!")
        self.eval_("""
      __complete_word = word ->
            path, dot, word = word.rpartition '.'
            completion_ns = globals!
            sorted $ map (path + dot +) $
                # Hide private attributes unless an underscore was typed.
                filter (w -> w.startswith word and (word or not (w.startswith '_'))) $ if
                    not path  => set Compiler.prefix | set BUILTINS | set completion_ns
                    otherwise => except
                        err => dir $ eval path completion_ns
                        err `isinstance` Exception => []""")

        # initializing dg repl:
        # -this project will be shared among all kernels
        # +will do bro!

    def do_complete(self, code_, cursor_pos_):
        code_ = code_[:cursor_pos_]
        real_cursor_pos_in_code_ = abs(cursor_pos_ - (code_.count(' ') + code_.count('\n')))
        splitted_code_ = code_.split()
        # LOL??
        #raise Exception('code:' + code_ + '\n' + 'cursor-pos:' + str(cursor_pos_) + '\n' + 'real-cursor-pos:' + str(real_cursor_pos_in_code_))
        z = 0
        splitted_code_f_ = ""
        for i in range(len(splitted_code_)):
            real_cursor_pos_in_code_ -= len(splitted_code_[i])
            if real_cursor_pos_in_code_ <= 0:
                splitted_code_f_ = splitted_code_[i]
                real_cursor_pos_end_ = len(splitted_code_f_)
                break

        completion_results_ = self.eval_('__complete_word ' + '"{}"'.format(splitted_code_f_))

        return {'status': 'ok',
                'matches': completion_results_,
                'cursor_start' : cursor_pos_,
                'cursor_end' : cursor_pos_ - real_cursor_pos_end_,
                'metadata' : {}}

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
                except (RuntimeError, TypeError, NameError,
                        AttributeError, ValueError,
                        dg.SyntaxError, ImportError) as e:
                    errorflag_ = True
                    eval_ = str(e)

                std_out_ = f.getvalue()

            ret_ = ''
            if len(std_out_) > 0:
                ret_ = str(std_out_) + '\n'

            if eval_ is not None:
                ret_ = ret_ + str(eval_)

            if isinstance(eval_, IPython.core.display.Markdown):
                data_ = eval_.data
                content_ = {
                    'source': 'kernel',
                    'data': {
                        'text/markdown': data_
                    },
                    'metadata' : {}
                }
                self.send_response(self.iopub_socket,
                                   'display_data', content_)
            elif isinstance(eval_, matplotlib.figure.Figure):
                fig_ = eval_
                png_ = self._to_png(fig_)
                [width_, height_] = fig_.get_size_inches()
                dpi_ = fig_.dpi
                content_ = {
                    'source': 'kernel',
                    'data': {
                        'image/png': png_
                    },
                    'metadata' : {
                        'image/png' : {
                            'width': width_ * dpi_,
                            'height': height_ * dpi_
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
