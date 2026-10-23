# Python_snippets

A bunch of code snippets and subroutines in Python 3, packaged within Jupyter notebooks. The code has been repurposed from various codes I have written for mostly personal use in my research work over more than a 10 year period - I have suitably modified Python 2 codes.
Each notebook will also contains sections generating test dataset(s), and a test run of the snippet/subroutine using the generated dataset(s).

## Setting up a virtual environment

The notebooks need a few third-party packages (NumPy, SciPy, Matplotlib and Jupyter). Installing them in a virtual environment keeps them separate from your system Python and from other projects, so versions don't clash and the setup can be reproduced on any machine.

Create and activate a virtual environment in the repository folder (Python 3 required):

```bash
python3 -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
```

With the virtual environment **activated**, install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

`requirements.txt` must be installed inside the activated virtual environment; otherwise the packages go into your system Python instead. Then start Jupyter from the same environment and open any notebook:

```bash
jupyter notebook
```

Run `deactivate` to leave the virtual environment. Next time, just activate it again with `source .venv/bin/activate` before starting Jupyter.

The `.spec` data files used by the 2D timeseries notebooks are stored with [Git LFS](https://git-lfs.com). Install Git LFS before cloning (or run `git lfs pull` after cloning) to get the actual data instead of small pointer files.
