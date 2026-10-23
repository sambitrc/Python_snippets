# Python_snippets

A bunch of code snippets and subroutines in Python 3, packaged within Jupyter notebooks. The code has been repurposed from various codes I have written for mostly personal use in my research work over more than a 10 year period - I have suitably modified Python 2 codes.
The reusable code lives as functions in `python_functions/`, and each notebook in `example_notebooks/` shows how to use them, either on generated test dataset(s) or on the real example data included in the repository.

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

## Functions

Each function has a docstring describing its parameters and return values (e.g. `help(power_spectrum)`).

### `python_functions/Analysis_functions.py`

| Function | What it does | Used in |
|---|---|---|
| `read_rpg_spec(filename, ts=0.1, chans=8192, ...)` | Reads an RPG FFT spectrometer `.spec` file into a (time stamps × channels) array, calibrated to mW | 2Dtimeseries_1, 2Dtimeseries_2 |
| `mean_stack(tms)` | Unweighted mean of a set of timeseries (one per row), ignoring NaNs | Stacking_timeseries |
| `median_stack(tms)` | Unweighted median of a set of timeseries, ignoring NaNs | Stacking_timeseries |
| `noise_weights(tms, n_edge=100, mad_threshold=5.0, power=2)` | Noise of each timeseries from its signal-free ends, rejection of outlying low-noise series, and normalized 1/rms² (or 1/rms) weights | Stacking_timeseries |
| `weighted_mean_stack(tms, wts)` | Weighted mean of a set of timeseries, skipping NaN weights and data | Stacking_timeseries |
| `autodifference(x, lag=1)` | (x[i] − x[i+lag]) / √2, whose rms estimates the white noise level | 2Dtimeseries_1 |
| `power_spectrum(x, dt)` | One-sided power spectral density, \|FFT\|² · dt, without the zero-frequency term | 2Dtimeseries_1, 2Dtimeseries_2 |
| `gain_match(x, ref)` | Rescales a timeseries so its mean matches that of a reference | 2Dtimeseries_2 |
| `difference_timeseries(x1, x2)` | Fits x2 = m·x1 + c and returns the difference (m·x1 + c − x2) / √2, with m and c | 2Dtimeseries_2 |

### `python_functions/plotting_functions.py`

| Function | What it does | Used in |
|---|---|---|
| `plot_with_transparency(x, y, yu, yd, color='cyan', alpha=0.2, filename=None, ...)` | Line plot with a semi-transparent band between yu and yd, optionally saved as PNG | Plots_with_transparency |
| `waterfall_plot(data, xlabel, ylabel, cbar_label=None, aspect=3, ...)` | 2D image (waterfall) plot of a 2D timeseries with a colour bar, optionally saved as PNG | 2Dtimeseries_1 |

Both plotting functions return the matplotlib `fig, ax`, so the plots can be customised further.

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
