"""
This is simplest possible kernel for ipurescript based on echokernel + pexpect
"""

import errno
import os
import signal
import subprocess
import sys

from ipykernel.kernelbase import Kernel
from pexpect import popen_spawn


class IPurescriptKernel(Kernel):
    """
    IPurescript: jupyter kernel for purescript
    """
    implementation = 'IPurescript'
    implementation_version = '1.0'
    language = 'purescript'
    language_version = '0.11.7'
    language_info = {
        'name': 'Purescript',
        'mimetype': 'text/plain',
        'file_extension': '.purs',
    }
    banner = "IPurescript kernel - awesomeness exceeds all limit!"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # initializing purescript project with pulp
        # this project will be shared among all kernels

        project_path = os.path.join(os.path.dirname(__file__), 'temp')
        try:
            os.makedirs(project_path)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

        exec_str = 'pulp.cmd' if sys.platform == 'win32' else 'pulp'
        subprocess.run([exec_str, 'init'], cwd=project_path)

        self.child = popen_spawn.PopenSpawn(
            exec_str + ' repl',
            cwd=project_path
        )
        self.child.expect('\n> ')

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            self.child.sendline(code)
            # waiting for prompt to show up
            self.child.expect('> ')
            response_text = bytes(self.child.before)
            if response_text == b'' or response_text[-1] == b'\n'[-1]:
                # means we got an actual prompt
                pass
            else:
                # means we got just a '> ' characters in the middle of a line
                # so we do another search until we find an actual prompt
                response_text += self.child.after
                self.child.expect('\n> ')
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
