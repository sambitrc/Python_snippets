"""Plotting functions used by the notebooks in this repository."""

from matplotlib import pyplot as plt


def plot_with_transparency(x, y, yu, yd, color='cyan', alpha=0.2,
                           filename=None, dpi=300, show=True):
    """Plot y against x with a semi-transparent band between yu and yd.

    Parameters
    ----------
    x, y : array_like
        Data for the central line.
    yu, yd : array_like
        Upper and lower edges of the shaded band.
    color : str
        Colour of the band.
    alpha : float
        Transparency of the band (0 = invisible, 1 = opaque).
    filename : str, optional
        If given, save the figure to this path as PNG.
    dpi : int
        Resolution used when saving.
    show : bool
        Call plt.show() at the end.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.fill_between(x, yu, yd, color=color, alpha=alpha)
    if filename is not None:
        fig.savefig(filename, dpi=dpi, format='png')
    if show:
        plt.show()
    return fig, ax


def waterfall_plot(data, xlabel='channel no.', ylabel='time stamp',
                   cbar_label=None, aspect=3, cmap=None, vmin=None, vmax=None,
                   filename=None, dpi=300, show=True):
    """Waterfall plot (2D image) of a 2D timeseries.

    Parameters
    ----------
    data : 2D array_like, shape (n_times, n_channels)
        Values to plot, one row per time stamp. Pass e.g. np.log10(data)
        to plot on a logarithmic scale.
    xlabel, ylabel : str
        Axis labels.
    cbar_label : str, optional
        Colour bar label.
    aspect : float or 'auto'
        Aspect ratio of the image pixels.
    cmap : str, optional
        Matplotlib colour map (default: matplotlib's default).
    vmin, vmax : float, optional
        Colour scale limits (default: data range).
    filename : str, optional
        If given, save the figure to this path as PNG.
    dpi : int
        Resolution used when saving.
    show : bool
        Call plt.show() at the end.

    Returns
    -------
    fig, ax : matplotlib Figure and Axes
    """
    fig, ax = plt.subplots()
    im = ax.imshow(data, aspect=aspect, interpolation='nearest',
                   cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    cbar = fig.colorbar(im, ax=ax)
    if cbar_label is not None:
        cbar.set_label(cbar_label)
    if filename is not None:
        fig.savefig(filename, dpi=dpi, format='png')
    if show:
        plt.show()
    return fig, ax
