"""__main__"""

from ipykernel.kernelapp import IPKernelApp
from . import IPurescriptKernel

IPKernelApp.launch_instance(kernel_class=IPurescriptKernel)
