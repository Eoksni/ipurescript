"""__main__"""

from ipykernel.kernelapp import IPKernelApp
from . import IdgKernel

IPKernelApp.launch_instance(kernel_class=IdgKernel)
