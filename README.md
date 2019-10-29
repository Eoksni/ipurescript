# IPurescript

This is a jupyter kernel for purescript. It is written as a wrapper kernel based on `ipykernel.kernelbase.Kernel`. 

It was tested on Windows, but should work on POSIX systems with little to no changes.

This project is in very early stage, but I already use it myself for learning `purescript`, 
so it might be usable enough for you as well ;)

** I don't have time anymore to work on this, feel free to continue it or start from scratch. **

# Install (for OS Windows)

First install `purescript`, so that you have `pulp` command in your shell. Then,

```
git clone https://github.com/Eoksni/ipurescript
cd ipurescript
jupyter kernelspec install ipurescript
```

It should give you something like
```
[InstallKernelSpec] Installed kernelspec ipurescript in C:\ProgramData\jupyter\kernels\ipurescript
```

Take that path `C:\ProgramData\jupyter\kernels` (without `ipurescript` part) and add it to `PYTHONPATH` environment variable.

Then you can run the jupyter normally

```
jupyter notebook
```
or
```
jupyter console --kernel ipurescript
```

# Important notes

On the first launch, the kernel will create and initialize a purescript 
project in directory `temp` at the path where the kernel was installed (ie `C:\ProgramData\jupyter\kernels\ipurescript\temp`).

This project directory is shared among all kernels instances. 

If you need additional `purescript` dependencies installed, you can do it normally,
treating this project directory as usual purescript project.

# Example notebook

[Example notebook](example.png)

# Features Supported

So far you can only run cells and it will display the output from the purescript REPL. Autocomplete or syntax highligthing or inspect do not work.

# Known bugs

- [ ] Multi-line input doesn't work
