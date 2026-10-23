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
