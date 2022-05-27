# IDg

This is a jupyter kernel for dg language. It is written as a wrapper kernel based on `ipykernel.kernelbase.Kernel`. 

This project is in relatively early stage.

Author: **I don't have time anymore to work on this, feel free to continue it or start from scratch.**
Me: Will do bro, for Dg language.

TODO: REST OF THE CONTENT WILL BE CHANGE

# Install: MacOS

# Install: Windows

First install `dg`, so that you have `dg` package in your python environment. Then,

```
git clone https://github.com/LeaveNhA/idg
cd ipurescript
jupyter kernelspec install idg
```

It should give you something like
```
[InstallKernelSpec] Installed kernelspec idg in C:\ProgramData\jupyter\kernels\idg
```

Take that path `C:\ProgramData\jupyter\kernels` (without `idg` part) and add it to `PYTHONPATH` environment variable.

Then you can run the jupyter normally

```
jupyter notebook
```
or
```
jupyter console --kernel idg
```

# Important notes

None.

# Example notebook

[Example notebook](example.gif)

# Features Supported

TODO

# Known bugs

Lots of, I believe? Please inform me with issues.
