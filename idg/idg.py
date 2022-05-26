"""
This is simplest possible kernel for dg based on echokernel + pexpect
"""

import errno
import os
import signal
import subprocess
import sys

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

        project_path = os.path.join(os.path.dirname(__file__), 'temp')
        try:
            os.makedirs(project_path)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

        # I don't care about the Windows or any
        # other Microsoft products at all! :))
        exec_str = 'python -m dg'
        subprocess.run([exec_str, 'init'], cwd=project_path)

        self.child = popen_spawn.PopenSpawn(
            exec_str, # yeap, no additional `-repl` str
            cwd=project_path
        )
        self.child.expect('\n>>> ')

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            self.child.sendline(code)
            # waiting for prompt to show up
            self.child.expect('...')
            response_text = bytes(self.child.before)
            if response_text == b'' or response_text[-1] == b'\n'[-1]:
                # means we got an actual prompt
                pass
            else:
                # means we got just a '> ' characters in the middle of a line
                # so we do another search until we find an actual prompt
                response_text += self.child.after
                self.child.expect('\n>>> ')
                response_text += self.child.before

            stream_content = {'name': 'stdout',
                              'text': response_text.decode('utf-8')}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def do_shutdown(self, restart):
        self.child.kill(signal.CTRL_C_EVENT)
