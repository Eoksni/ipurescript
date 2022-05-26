"""
This is simplest possible kernel for dg based on echokernel + pexpect
"""

import errno
import os
import signal
import subprocess
import sys
import dg

from ipykernel.kernelbase import Kernel
from pexpect import popen_spawn


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
        'mimetype': 'text/plain',
        'file_extension': '.dg',
    }
    banner = "Idg kernel - awesomeness exceeds all limit!"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # initializing dg repl:
        # -this project will be shared among all kernels
        # +will do bro!

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            ret_ = eval(dg.compile(code))

            stream_content = {'name': 'stdout',
                              'text': str(ret_)}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }
