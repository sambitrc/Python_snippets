# Python_snippets

A bunch of code snippets and subroutines in Python 3, packaged within Jupyter notebooks. The code has been repurposed from various codes I have written for mostly personal use in my research work over more than a 10 year period - I have suitably modified Python 2 codes.
Each notebook will also contains sections generating test dataset(s), and a test run of the snippet/subroutine using the generated dataset(s).

## Repository layout

```
Python_snippets/
├── example_notebooks/      # Jupyter notebooks, and the data files they use
│   ├── Plots_with_transparency.ipynb
│   ├── Stacking_timeseries.ipynb
│   ├── 2Dtimeseries_1_Visualization_Properties.ipynb
│   ├── 2Dtimeseries_2_Difference_timeseries.ipynb
│   ├── RPGFFTSchanA.spec, RPGFFTSchanB.spec   # real spectrometer data (Git LFS)
│   └── sinewtransparency.png                  # output of Plots_with_transparency.ipynb
├── python_functions/       # reusable functions called by the notebooks
│   ├── plotting_functions.py
│   └── Analysis_functions.py
├── requirements.txt
└── README.md
```

The notebooks import the functions from `python_functions/` by adding that folder to the Python path in their first code cell. This uses a path relative to the notebook (`../python_functions`), so run each notebook from inside `example_notebooks/`, which Jupyter and VS Code do by default. The functions can also be used in your own scripts: add `python_functions/` to your Python path, then e.g. `from Analysis_functions import mean_stack`.

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

`requirements.txt` must be installed inside the activated virtual environment; otherwise the packages go into your system Python instead. Then start Jupyter from the same environment and open any notebook in `example_notebooks/`:

```bash
jupyter notebook
```

Run `deactivate` to leave the virtual environment. Next time, just activate it again with `source .venv/bin/activate` before starting Jupyter.

The `.spec` data files in `example_notebooks/`, used by the 2D timeseries notebooks, are stored with [Git LFS](https://git-lfs.com). Install Git LFS before cloning (or run `git lfs pull` after cloning) to get the actual data instead of small pointer files.
